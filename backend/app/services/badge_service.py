from sqlalchemy.orm import Session
from app.models import Badge, PlayerBadge, RoomCompletion, Attempt
from datetime import date


def _player_has_badge(player_id: int, badge_id: str, db: Session) -> bool:
    return (
        db.query(PlayerBadge)
        .filter_by(player_id=player_id, badge_id=badge_id)
        .first()
        is not None
    )


def _grant_badge(player_id: int, badge_id: str, db: Session) -> Badge | None:
    badge = db.query(Badge).filter_by(id=badge_id).first()
    if badge is None:
        return None
    pb = PlayerBadge(player_id=player_id, badge_id=badge_id)
    db.add(pb)
    db.flush()
    return badge


def _collect_progress_candidates(player_id: int, context: dict[str, object], db: Session) -> list[str]:
    candidates: list[str] = []
    if not context.get("room_cleared"):
        return candidates

    total_rooms = db.query(RoomCompletion).filter_by(player_id=player_id).count()
    if total_rooms == 1:
        candidates.append("first_step")

    zone = context.get("zone_number")
    if context.get("zone_cleared") and isinstance(zone, int):
        candidates.append(f"zone{zone}_clear")
        boss_completions = (
            db.query(RoomCompletion)
            .filter(
                RoomCompletion.player_id == player_id,
                RoomCompletion.room_number == 6,
            )
            .count()
        )
        if boss_completions >= 8:
            candidates.append("dungeon_master")

    return candidates


def _collect_skill_candidates(context: dict[str, object]) -> list[str]:
    candidates: list[str] = []
    if not (context.get("correct") and context.get("room_cleared")):
        return candidates

    attempts = int(str(context.get("attempts_in_room", 99)))
    time_ms = int(str(context.get("time_ms", 99999)))

    if attempts <= 1:
        candidates.append("flawless_room")
    if context.get("is_boss") and attempts <= 1:
        candidates.append("boss_first_try")
    if time_ms < 20000:
        candidates.append("speedrun_room")

    return candidates


def _collect_combo_candidates(context: dict[str, object]) -> list[str]:
    candidates: list[str] = []
    combo = int(str(context.get("combo", 1)))
    if combo >= 5:
        candidates.append("combo_5")
    if combo >= 10:
        candidates.append("combo_10")
    if combo >= 20:
        candidates.append("combo_20")
    return candidates


def _collect_bug_hunter_candidate(player_id: int, context: dict[str, object], db: Session) -> list[str]:
    if context.get("challenge_type") != "find_bug" or not context.get("correct"):
        return []
    bug_correct = (
        db.query(Attempt)
        .filter(
            Attempt.player_id == player_id,
            Attempt.correct == True,  # noqa: E712
            Attempt.concept_tags.contains("find_bug"),
        )
        .count()
    )
    return ["bug_hunter"] if bug_correct >= 10 else []


BADGE_PRIORITY: list[str] = [
    "dungeon_master",
    "zone8_clear", "zone7_clear", "zone6_clear", "zone5_clear",
    "zone4_clear", "zone3_clear", "zone2_clear", "zone1_clear",
    "first_step", "boss_first_try", "flawless_room",
    "combo_20", "combo_10", "combo_5",
    "speedrun_room", "bug_hunter",
]


def check_and_grant(player_id: int, context: dict[str, object], db: Session) -> Badge | None:
    candidates: list[str] = []
    candidates += _collect_progress_candidates(player_id, context, db)
    candidates += _collect_skill_candidates(context)
    candidates += _collect_combo_candidates(context)
    candidates += _collect_bug_hunter_candidate(player_id, context, db)

    candidate_set = set(candidates)
    for badge_id in BADGE_PRIORITY:
        if badge_id in candidate_set and not _player_has_badge(player_id, badge_id, db):
            return _grant_badge(player_id, badge_id, db)

    return None
