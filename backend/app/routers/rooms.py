from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Player, Attempt
from app.dependencies import get_current_player
from app.schemas import AttemptRequest, AttemptResponse, BadgeOut
from app.services.attempt_service import process_attempt
from app.services.badge_service import check_and_grant
from app.content.challenges_data import CHALLENGES
from app.content.challenge_types import ChallengeData

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/{room_id}/attempt", response_model=AttemptResponse)
def submit_attempt(
    room_id: str,
    data: AttemptRequest,
    player: Player = Depends(get_current_player),
    db: Session = Depends(get_db),
) -> AttemptResponse:
    ch: ChallengeData | None = CHALLENGES.get(room_id)
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

    total_attempts_in_room: int = (
        db.query(Attempt)
        .filter_by(player_id=player.id, challenge_id=room_id)
        .count()
    )
    granted = check_and_grant(
        player_id=player.id,
        context={
            "correct": result["correct"],
            "room_id": room_id,
            "zone_number": ch["zone"],
            "room_number": ch["room"],
            "is_boss": ch["is_boss"],
            "is_mini_boss": ch["is_mini_boss"],
            "room_cleared": result["room_cleared"],
            "zone_cleared": result["zone_cleared"],
            "combo": result["combo"],
            "challenge_type": ch["challenge_type"],
            "attempts_in_room": total_attempts_in_room,
            "time_ms": data.time_ms,
        },
        db=db,
    )
    db.commit()

    badge_out: BadgeOut | None = None
    if granted:
        first = granted[0]
        badge_out = BadgeOut(
            id=str(first.id),
            name=str(first.name),
            description=str(first.description),
            icon_key=str(first.icon_key),
            category=str(first.category),
            secret=bool(first.secret),
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
        is_mini_boss=result["is_mini_boss"],
    )
