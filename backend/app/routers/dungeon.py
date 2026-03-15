from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Player, RoomCompletion
from app.dependencies import get_current_player
from app.content.challenges_data import CHALLENGES, ZONES
from app.schemas import ZoneOut, RoomOut

router = APIRouter(prefix="/dungeon", tags=["dungeon"])

ROOM_TYPE_NAMES: dict[str, str] = {
    "trace_value": "Trace l'Exécution",
    "find_bug": "Trouve le Bug",
    "match_types": "Associe les Types",
    "sort_order": "Remets en Ordre",
    "fill_blank": "Complète le Code",
    "memory_map": "Carte Mémoire",
}


def _get_player_completions(player_id: int, db: Session) -> set[str]:
    rows = db.query(RoomCompletion.room_id).filter_by(player_id=player_id).all()
    return {row.room_id for row in rows}


def _get_player_completions_with_attempts(player_id: int, db: Session) -> dict[str, int]:
    rows = (
        db.query(RoomCompletion.room_id, RoomCompletion.attempts_taken)
        .filter_by(player_id=player_id)
        .all()
    )
    return {row.room_id: row.attempts_taken for row in rows}


@router.get("/zones", response_model=list[ZoneOut])
def get_zones(
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> list[ZoneOut]:
    current_zone: int = int(player.stats.current_zone)
    completions = _get_player_completions(player.id, db)
    result: list[ZoneOut] = []
    for zone in ZONES:
        z: int = int(zone["zone_number"])
        zone_rooms = [rid for rid, ch in CHALLENGES.items() if ch.get("zone") == z]
        cleared = sum(1 for rid in zone_rooms if rid in completions)
        boss_id = f"z{z:02d}_r06"
        result.append(ZoneOut(
            zone_number=z,
            name=str(zone["name"]),
            theme=str(zone["theme"]),
            emoji=str(zone["emoji"]),
            rooms_total=len(zone_rooms),
            rooms_cleared=cleared,
            is_unlocked=z <= current_zone,
            is_boss_cleared=boss_id in completions,
            boss_name=str(zone["boss_name"]),
        ))
    return result


@router.get("/zones/{zone_number}/rooms", response_model=list[RoomOut])
def get_rooms(
    zone_number: int,
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> list[RoomOut]:
    if zone_number < 1 or zone_number > 8:
        raise HTTPException(status_code=404, detail="Zone inconnue")

    completions = _get_player_completions_with_attempts(player.id, db)
    zone_rooms = sorted(
        [(rid, ch) for rid, ch in CHALLENGES.items() if ch.get("zone") == zone_number],
        key=lambda x: int(str(x[1].get("room", 0))),
    )
    result: list[RoomOut] = []
    for rid, ch in zone_rooms:
        name = str(ch.get("title", ROOM_TYPE_NAMES.get(str(ch.get("challenge_type", "")), "Salle")))
        result.append(RoomOut(
            room_id=rid,
            zone_number=int(str(ch.get("zone", zone_number))),
            room_number=int(str(ch.get("room", 0))),
            name=name,
            challenge_type=str(ch.get("challenge_type", "")),
            is_boss=bool(ch.get("is_boss", False)),
            is_cleared=rid in completions,
            attempts_taken=completions.get(rid, 0),
        ))
    return result


@router.get("/rooms/{room_id}")
def get_room(
    room_id: str,
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    ch = CHALLENGES.get(room_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Salle inconnue")

    zone = int(str(ch.get("zone", 0)))
    current_zone = int(player.stats.current_zone)
    if zone > current_zone:
        raise HTTPException(status_code=403, detail="Cette zone n'est pas encore débloquée")

    room_num = int(str(ch.get("room", 1)))
    if room_num > 1:
        prev_room_id = f"z{zone:02d}_r{room_num - 1:02d}"
        cleared = _get_player_completions(player.id, db)
        if prev_room_id not in cleared:
            raise HTTPException(status_code=403, detail="Complète les salles précédentes d'abord")

    completions = _get_player_completions(player.id, db)
    return {
        "room_id": room_id,
        "zone_number": zone,
        "room_number": room_num,
        "is_boss": bool(ch.get("is_boss", False)),
        "challenge_type": str(ch.get("challenge_type", "")),
        "title": str(ch.get("title", "")),
        "question_prompt": str(ch.get("question_prompt", "")),
        "concept_tags": ch.get("concept_tags", []),
        "difficulty": int(str(ch.get("difficulty", 1))),
        "payload": ch.get("payload", {}),
        "is_cleared": room_id in completions,
    }
