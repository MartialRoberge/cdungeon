from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Player, Attempt
from app.dependencies import get_current_player
from app.schemas import AttemptRequest, AttemptResponse, BadgeOut
from app.services.attempt_service import process_attempt
from app.services.badge_service import check_and_grant
from app.content.challenges_data import CHALLENGES

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/{room_id}/attempt", response_model=AttemptResponse)
def submit_attempt(
    room_id: str,
    data: AttemptRequest,
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> AttemptResponse:
    ch = CHALLENGES.get(room_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Salle inconnue")

    result = process_attempt(
        player=player,
        room_id=room_id,
        raw_answer=data.answer,
        combo=data.combo,
        time_ms=data.time_ms,
        db=db,
    )

    correct_attempts = (
        db.query(Attempt)
        .filter_by(player_id=player.id, challenge_id=room_id, correct=True)
        .count()
    )
    granted = check_and_grant(
        player_id=player.id,
        context={
            "correct": result["correct"],
            "room_id": room_id,
            "zone_number": ch.get("zone"),
            "is_boss": ch.get("is_boss"),
            "room_cleared": result["room_cleared"],
            "zone_cleared": result["zone_cleared"],
            "combo": result["combo"],
            "challenge_type": ch.get("challenge_type"),
            "attempts_in_room": correct_attempts,
            "time_ms": data.time_ms,
        },
        db=db,
    )
    db.commit()

    badge_out: BadgeOut | None = None
    if granted is not None:
        badge_out = BadgeOut(
            id=str(granted.id),
            name=str(granted.name),
            description=str(granted.description),
            icon_key=str(granted.icon_key),
            category=str(granted.category),
            secret=bool(granted.secret),
            earned=True,
            earned_at=None,
        )

    return AttemptResponse(
        correct=result["correct"],
        explanation=result["explanation"],
        xp_earned=result["xp_earned"],
        new_total_xp=result["new_total_xp"],
        new_level=result["new_level"],
        combo=result["combo"],
        hint_scroll=result["hint_scroll"],
        badge_unlocked=badge_out,
        room_cleared=result["room_cleared"],
        zone_cleared=result["zone_cleared"],
    )
