from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Player, Badge, PlayerBadge
from app.schemas import PlayerMe, BadgeOut
from app.dependencies import get_current_player

router = APIRouter(prefix="/player", tags=["player"])


@router.get("/me", response_model=PlayerMe)
def get_me(player: Player = Depends(get_current_player)):
    s = player.stats
    return PlayerMe(
        id=player.id,
        username=player.username,
        xp=s.xp,
        level=s.level,
        current_zone=s.current_zone,
        daily_streak=s.daily_streak,
        best_combo=s.best_combo,
        total_attempts=s.total_attempts,
        total_correct=s.total_correct,
    )


@router.get("/badges", response_model=list[BadgeOut])
def get_badges(player: Player = Depends(get_current_player), db: Session = Depends(get_db)):
    all_badges = db.query(Badge).all()
    earned_map = {pb.badge_id: pb.earned_at for pb in player.badges}
    result = []
    for b in all_badges:
        if b.secret and b.id not in earned_map:
            continue  # Hide secret badges until earned
        result.append(BadgeOut(
            id=b.id, name=b.name, description=b.description,
            icon_key=b.icon_key, category=b.category, secret=b.secret,
            earned=b.id in earned_map,
            earned_at=earned_map.get(b.id),
        ))
    return result
