import json
from typing import TypedDict
from sqlalchemy.orm import Session
from app.models import Player, PlayerStats, RoomCompletion, Attempt, ConceptAccuracy
from app.content.challenges_data import CHALLENGES


BASE_XP: dict[int, int] = {1: 10, 2: 15, 3: 25}
BOSS_MULTIPLIER: int = 3


class AttemptResult(TypedDict):
    correct: bool
    explanation: str
    xp_earned: int
    new_total_xp: int
    new_level: int | None
    combo: int
    hint_scroll: str | None
    room_cleared: bool
    zone_cleared: bool


def xp_for_level(level: int) -> int:
    return 100 * level + 25 * level * (level - 1)


def compute_xp(difficulty: int, is_boss: bool, combo: int) -> int:
    base: int = BASE_XP.get(difficulty, 10)
    combo_bonus: float = min(combo * 0.1, 1.0)
    xp: float = base * (1.0 + combo_bonus)
    if is_boss:
        xp *= BOSS_MULTIPLIER
    return round(xp)


def check_level_up(stats: PlayerStats) -> int | None:
    new_level: int = int(stats.level)
    while stats.xp >= xp_for_level(new_level + 1):
        new_level += 1
    if new_level > stats.level:
        stats.level = new_level
        return new_level
    return None


def validate_answer(challenge: dict[str, object], raw_answer: object) -> bool:
    ctype = str(challenge.get("challenge_type", ""))
    payload = challenge.get("payload")
    if not isinstance(payload, dict):
        return False
    correct_answer = payload.get("correct_answer")

    if ctype in ("fill_blank", "trace_value"):
        return str(raw_answer) == str(correct_answer)

    if ctype == "find_bug":
        try:
            return int(str(raw_answer)) == int(str(correct_answer))
        except (ValueError, TypeError):
            return False

    if ctype == "match_types":
        if not isinstance(raw_answer, dict):
            return False
        return dict(raw_answer) == correct_answer

    if ctype == "sort_order":
        if not isinstance(raw_answer, list):
            return False
        return list(raw_answer) == correct_answer

    if ctype == "memory_map":
        return str(raw_answer) == str(correct_answer)

    return False


def _get_challenge(room_id: str) -> dict[str, object]:
    challenge: dict[str, object] | None = CHALLENGES.get(room_id)
    if challenge is None:
        raise ValueError(f"Unknown room: {room_id}")
    return challenge


def _is_room_cleared(player_id: int, room_id: str, db: Session) -> bool:
    return (
        db.query(RoomCompletion)
        .filter_by(player_id=player_id, room_id=room_id)
        .first()
        is not None
    )


def _award_xp(stats: PlayerStats, challenge: dict[str, object], combo: int) -> tuple[int, int | None]:
    difficulty = int(str(challenge.get("difficulty", 1)))
    is_boss = bool(challenge.get("is_boss", False))
    xp_earned = compute_xp(difficulty, is_boss, combo)
    stats.xp += xp_earned
    new_level = check_level_up(stats)
    if combo > int(stats.best_combo):
        stats.best_combo = combo
    return xp_earned, new_level


def _log_attempt(
    player_id: int,
    room_id: str,
    challenge: dict[str, object],
    correct: bool,
    time_ms: int,
    combo: int,
    db: Session,
) -> None:
    tags = challenge.get("concept_tags", [])
    record = Attempt(
        player_id=player_id,
        challenge_id=room_id,
        concept_tags=json.dumps(tags),
        correct=correct,
        time_ms=time_ms,
        combo_at_time=combo,
    )
    db.add(record)


def _update_concept_accuracy(
    player_id: int,
    challenge: dict[str, object],
    correct: bool,
    db: Session,
) -> None:
    tags = challenge.get("concept_tags")
    if not isinstance(tags, list):
        return
    for tag in tags:
        tag_str = str(tag)
        acc = (
            db.query(ConceptAccuracy)
            .filter_by(player_id=player_id, concept_tag=tag_str)
            .first()
        )
        if acc is None:
            acc = ConceptAccuracy(player_id=player_id, concept_tag=tag_str, total=0, correct=0)
            db.add(acc)
        acc.total += 1
        if correct:
            acc.correct += 1


def _record_room_completion(
    player_id: int,
    room_id: str,
    challenge: dict[str, object],
    xp_earned: int,
    db: Session,
) -> tuple[bool, bool]:
    zone_num = int(str(challenge.get("zone", 0)))
    room_num = int(str(challenge.get("room", 0)))

    attempts_taken = (
        db.query(Attempt)
        .filter_by(player_id=player_id, challenge_id=room_id)
        .count()
    )
    completion = RoomCompletion(
        player_id=player_id,
        room_id=room_id,
        zone_number=zone_num,
        room_number=room_num,
        attempts_taken=attempts_taken,
        xp_earned=xp_earned,
    )
    db.add(completion)
    db.flush()

    zone_room_count = sum(1 for ch in CHALLENGES.values() if ch.get("zone") == zone_num)
    cleared_in_zone = (
        db.query(RoomCompletion)
        .filter(
            RoomCompletion.player_id == player_id,
            RoomCompletion.zone_number == zone_num,
        )
        .count()
    )
    zone_cleared = cleared_in_zone >= zone_room_count
    return True, zone_cleared


def _unlock_next_zone(stats: PlayerStats, challenge: dict[str, object]) -> None:
    zone_num = int(str(challenge.get("zone", 0)))
    next_zone = min(zone_num + 1, 8)
    if int(stats.current_zone) <= zone_num:
        stats.current_zone = next_zone


def check_adaptive_hint(player_id: int, challenge: dict[str, object], db: Session) -> str | None:
    tags = challenge.get("concept_tags")
    if not isinstance(tags, list):
        return None
    for tag in tags:
        tag_str = str(tag)
        acc = (
            db.query(ConceptAccuracy)
            .filter_by(player_id=player_id, concept_tag=tag_str)
            .first()
        )
        if acc is not None and int(acc.total) >= 2:
            ratio: float = int(acc.correct) / int(acc.total)
            if ratio < 0.5:
                hint = challenge.get("hint")
                return str(hint) if hint else None
    return None


def process_attempt(
    player: Player,
    room_id: str,
    raw_answer: object,
    combo: int,
    time_ms: int,
    db: Session,
) -> AttemptResult:
    challenge = _get_challenge(room_id)
    stats: PlayerStats = player.stats

    correct = validate_answer(challenge, raw_answer)
    already_cleared = _is_room_cleared(player.id, room_id, db)

    stats.total_attempts += 1
    if correct:
        stats.total_correct += 1

    xp_earned: int = 0
    new_level: int | None = None
    if correct and not already_cleared:
        xp_earned, new_level = _award_xp(stats, challenge, combo)

    _log_attempt(player.id, room_id, challenge, correct, time_ms, combo, db)
    _update_concept_accuracy(player.id, challenge, correct, db)

    room_cleared = False
    zone_cleared = False
    if correct and not already_cleared:
        room_cleared, zone_cleared = _record_room_completion(
            player.id, room_id, challenge, xp_earned, db
        )
        if zone_cleared:
            _unlock_next_zone(stats, challenge)

    db.commit()

    hint_scroll: str | None = None
    if not correct:
        hint_scroll = check_adaptive_hint(player.id, challenge, db)

    return AttemptResult(
        correct=correct,
        explanation=str(challenge.get("explanation", "")),
        xp_earned=xp_earned,
        new_total_xp=int(stats.xp),
        new_level=new_level,
        combo=combo + 1 if correct else 1,
        hint_scroll=hint_scroll,
        room_cleared=room_cleared,
        zone_cleared=zone_cleared,
    )
