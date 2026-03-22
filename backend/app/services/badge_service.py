from sqlalchemy.orm import Session
from app.models import Badge, PlayerBadge, RoomCompletion, Attempt
from app.content.challenges_data import CHALLENGES
from app.content.challenge_types import ZONE_COUNT, ROOM_COUNT_PER_ZONE


def _player_has_badge(player_id: int, badge_id: str, db: Session) -> bool:
    return (
        db.query(PlayerBadge)
        .filter_by(player_id=player_id, badge_id=badge_id)
        .first()
        is not None
    )


def _grant_badge(player_id: int, badge_id: str, db: Session) -> Badge | None:
    badge: Badge | None = db.query(Badge).filter_by(id=badge_id).first()
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

    total_rooms: int = db.query(RoomCompletion).filter_by(player_id=player_id).count()
    if total_rooms == 1:
        candidates.append("first_step")

    # Halfway badge: 60 rooms cleared
    if total_rooms >= 60:
        candidates.append("halfway")

    zone = context.get("zone_number")
    if context.get("zone_cleared") and isinstance(zone, int):
        candidates.append(f"zone{zone}_clear")
        # Dungeon master: count zones fully cleared
        zones_cleared: int = 0
        for z in range(1, ZONE_COUNT + 1):
            zone_room_count: int = sum(1 for ch in CHALLENGES.values() if ch["zone"] == z)
            cleared_in_zone: int = (
                db.query(RoomCompletion)
                .filter(
                    RoomCompletion.player_id == player_id,
                    RoomCompletion.zone_number == z,
                )
                .count()
            )
            if cleared_in_zone >= zone_room_count:
                zones_cleared += 1
        if zones_cleared >= ZONE_COUNT:
            candidates.append("dungeon_master")

    # Mini-boss badges
    if context.get("is_mini_boss") and isinstance(zone, int):
        room_number = context.get("room_number")
        if room_number == 8:
            candidates.append(f"zone{zone}_miniboss_1")
        elif room_number == 12:
            candidates.append(f"zone{zone}_miniboss_2")

    return candidates


def _collect_skill_candidates(player_id: int, context: dict[str, object], db: Session) -> list[str]:
    candidates: list[str] = []
    if not (context.get("correct") and context.get("room_cleared")):
        return candidates

    attempts: int = int(str(context.get("attempts_in_room", 99)))
    time_ms: int = int(str(context.get("time_ms", 99999)))

    if attempts <= 1:
        candidates.append("flawless_room")
    is_boss: bool = bool(context.get("is_boss"))
    is_mini_boss: bool = bool(context.get("is_mini_boss"))
    if (is_boss or is_mini_boss) and attempts <= 1:
        candidates.append("boss_first_try")
    if time_ms < 20000:
        candidates.append("speedrun_room")

    # Perfectionist: all rooms cleared with attempts_taken == 1
    total_rooms: int = ZONE_COUNT * ROOM_COUNT_PER_ZONE
    perfect_rooms: int = (
        db.query(RoomCompletion)
        .filter(
            RoomCompletion.player_id == player_id,
            RoomCompletion.attempts_taken == 1,
        )
        .count()
    )
    if perfect_rooms >= total_rooms:
        candidates.append("perfectionist")

    return candidates


def _collect_combo_candidates(context: dict[str, object]) -> list[str]:
    candidates: list[str] = []
    combo: int = int(str(context.get("combo", 1)))
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
    find_bug_ids: list[str] = [rid for rid, ch in CHALLENGES.items() if ch["challenge_type"] == "find_bug"]
    bug_correct: int = (
        db.query(Attempt)
        .filter(
            Attempt.player_id == player_id,
            Attempt.correct == True,  # noqa: E712
            Attempt.challenge_id.in_(find_bug_ids),
        )
        .count()
    )
    return ["bug_hunter"] if bug_correct >= 10 else []


BADGE_PRIORITY: list[str] = [
    "dungeon_master",
    "zone8_clear", "zone7_clear", "zone6_clear", "zone5_clear",
    "zone4_clear", "zone3_clear", "zone2_clear", "zone1_clear",
    "halfway",
    "zone8_miniboss_2", "zone8_miniboss_1",
    "zone7_miniboss_2", "zone7_miniboss_1",
    "zone6_miniboss_2", "zone6_miniboss_1",
    "zone5_miniboss_2", "zone5_miniboss_1",
    "zone4_miniboss_2", "zone4_miniboss_1",
    "zone3_miniboss_2", "zone3_miniboss_1",
    "zone2_miniboss_2", "zone2_miniboss_1",
    "zone1_miniboss_2", "zone1_miniboss_1",
    "first_step", "boss_first_try", "flawless_room",
    "perfectionist",
    "combo_20", "combo_10", "combo_5",
    "speedrun_room", "bug_hunter",
]


def check_and_grant(player_id: int, context: dict[str, object], db: Session) -> list[Badge]:
    candidates: list[str] = []
    candidates += _collect_progress_candidates(player_id, context, db)
    candidates += _collect_skill_candidates(player_id, context, db)
    candidates += _collect_combo_candidates(context)
    candidates += _collect_bug_hunter_candidate(player_id, context, db)

    candidate_set: set[str] = set(candidates)
    granted: list[Badge] = []
    for badge_id in BADGE_PRIORITY:
        if badge_id in candidate_set and not _player_has_badge(player_id, badge_id, db):
            badge: Badge | None = _grant_badge(player_id, badge_id, db)
            if badge is not None:
                granted.append(badge)

    return granted
