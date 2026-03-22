from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Player, RoomCompletion, ConceptAccuracy
from app.dependencies import get_current_player
from app.content.challenges_data import CHALLENGES, ZONES
from app.content.challenge_types import (
    ChallengeData,
    ZoneData,
    get_boss_room_id,
    get_mini_boss_room_ids,
)
from app.schemas import ZoneOut, RoomOut, OrbContext

router = APIRouter(prefix="/dungeon", tags=["dungeon"])

ROOM_TYPE_NAMES: dict[str, str] = {
    "trace_value": "Trace l'Execution",
    "find_bug": "Trouve le Bug",
    "match_types": "Associe les Types",
    "sort_order": "Remets en Ordre",
    "fill_blank": "Complete le Code",
    "memory_map": "Carte Memoire",
}


def _get_player_completions(player_id: int, db: Session) -> set[str]:
    rows = db.query(RoomCompletion.room_id).filter_by(player_id=player_id).all()
    return {str(row.room_id) for row in rows}


def _get_player_completions_with_attempts(player_id: int, db: Session) -> dict[str, int]:
    rows = (
        db.query(RoomCompletion.room_id, RoomCompletion.attempts_taken)
        .filter_by(player_id=player_id)
        .all()
    )
    return {str(row.room_id): int(row.attempts_taken) for row in rows}


def _build_orb_context(player_id: int, challenge: ChallengeData, db: Session) -> OrbContext:
    tags: list[str] = challenge["concept_tags"]
    accuracy: dict[str, float] = {}
    for tag in tags:
        acc = (
            db.query(ConceptAccuracy)
            .filter_by(player_id=player_id, concept_tag=tag)
            .first()
        )
        if acc is not None and int(acc.total) > 0:
            accuracy[tag] = int(acc.correct) / int(acc.total)
        else:
            accuracy[tag] = 0.0
    return OrbContext(
        concept_tags=tags,
        difficulty=challenge["difficulty"],
        player_accuracy=accuracy,
    )


@router.get("/zones", response_model=list[ZoneOut])
def get_zones(
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> list[ZoneOut]:
    current_zone: int = int(player.stats.current_zone)
    completions: set[str] = _get_player_completions(player.id, db)
    result: list[ZoneOut] = []
    for zone in ZONES:
        z: int = zone["zone_number"]
        zone_rooms: list[str] = [rid for rid, ch in CHALLENGES.items() if ch["zone"] == z]
        cleared: int = sum(1 for rid in zone_rooms if rid in completions)
        boss_id: str = get_boss_room_id(z)
        mb1_id, mb2_id = get_mini_boss_room_ids(z)
        result.append(ZoneOut(
            zone_number=z,
            name=zone["name"],
            theme=zone["theme"],
            emoji=zone["emoji"],
            rooms_total=len(zone_rooms),
            rooms_cleared=cleared,
            is_unlocked=z <= current_zone,
            is_boss_cleared=boss_id in completions,
            boss_name=zone["boss_name"],
            has_mini_boss_1=mb1_id in completions,
            has_mini_boss_2=mb2_id in completions,
        ))
    return result


@router.get("/zones/{zone_number}/rooms", response_model=list[RoomOut])
def get_rooms(
    zone_number: int,
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> list[RoomOut]:
    if zone_number < 1 or zone_number > len(ZONES):
        raise HTTPException(status_code=404, detail="Zone inconnue")

    completions: dict[str, int] = _get_player_completions_with_attempts(player.id, db)
    cleared_set: set[str] = set(completions.keys())
    zone_rooms: list[tuple[str, ChallengeData]] = sorted(
        [(rid, ch) for rid, ch in CHALLENGES.items() if ch["zone"] == zone_number],
        key=lambda x: x[1]["room"],
    )
    result: list[RoomOut] = []
    for rid, ch in zone_rooms:
        room_num: int = ch["room"]
        # A room is locked if the previous room in the zone is not cleared
        is_locked: bool = False
        if room_num > 1:
            prev_room_id: str = f"z{zone_number:02d}_r{room_num - 1:02d}"
            if prev_room_id not in cleared_set:
                is_locked = True

        name: str = ch["title"]
        result.append(RoomOut(
            room_id=rid,
            zone_number=ch["zone"],
            room_number=room_num,
            name=name,
            challenge_type=ch["challenge_type"],
            is_boss=ch["is_boss"],
            is_mini_boss=ch["is_mini_boss"],
            is_cleared=rid in cleared_set,
            is_locked=is_locked,
            attempts_taken=completions.get(rid, 0),
        ))
    return result


@router.get("/rooms/{room_id}")
def get_room(
    room_id: str,
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    ch: ChallengeData | None = CHALLENGES.get(room_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Salle inconnue")

    zone: int = ch["zone"]
    current_zone: int = int(player.stats.current_zone)
    if zone > current_zone:
        raise HTTPException(status_code=403, detail="Cette zone n'est pas encore debloquee")

    completions: set[str] = _get_player_completions(player.id, db)

    room_num: int = ch["room"]
    if room_num > 1:
        prev_room_id: str = f"z{zone:02d}_r{room_num - 1:02d}"
        if prev_room_id not in completions:
            raise HTTPException(status_code=403, detail="Complete les salles precedentes d'abord")

    orb_context: OrbContext = _build_orb_context(player.id, ch, db)

    return {
        "room_id": room_id,
        "zone_number": zone,
        "room_number": room_num,
        "is_boss": ch["is_boss"],
        "is_mini_boss": ch["is_mini_boss"],
        "challenge_type": ch["challenge_type"],
        "title": ch["title"],
        "question_prompt": ch["question_prompt"],
        "concept_tags": ch["concept_tags"],
        "difficulty": ch["difficulty"],
        "payload": ch["payload"],
        "is_cleared": room_id in completions,
        "orb_context": orb_context.model_dump(),
    }
