from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Player, Badge, PlayerBadge
from app.dependencies import get_current_player
from app.services.share_service import generate_share_card

router = APIRouter(prefix="/share", tags=["share"])


@router.get("/me")
def share_my_card(player: Player = Depends(get_current_player), db: Session = Depends(get_db)):
    s = player.stats
    earned = db.query(Badge).join(PlayerBadge).filter(PlayerBadge.player_id == player.id).all()
    player_data = {
        "id": player.id,
        "username": player.username,
        "level": s.level,
        "xp": s.xp,
        "current_zone": s.current_zone,
        "best_combo": s.best_combo,
        "total_attempts": s.total_attempts,
        "total_correct": s.total_correct,
        "badges": [{"name": b.name, "icon_key": b.icon_key} for b in earned],
    }
    path = generate_share_card(player_data)
    return FileResponse(path, media_type="image/png", filename=f"cdungeon_{player.username}.png")
