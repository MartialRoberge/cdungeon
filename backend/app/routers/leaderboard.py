from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Player, PlayerStats
from app.dependencies import get_current_player

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("")
def get_leaderboard(
    by: str = Query("xp", enum=["xp", "combo", "streak"]),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    player: Player = Depends(get_current_player),
):
    sort_col = {"xp": PlayerStats.xp, "combo": PlayerStats.best_combo, "streak": PlayerStats.daily_streak}[by]
    rows = (
        db.query(Player.username, PlayerStats.level, sort_col.label("value"))
        .join(PlayerStats, Player.id == PlayerStats.player_id)
        .order_by(sort_col.desc())
        .limit(limit)
        .all()
    )
    result = []
    for i, row in enumerate(rows):
        result.append({
            "rank": i + 1,
            "username": row.username,
            "level": row.level,
            "value": row.value,
            "is_me": row.username == player.username,
        })
    return result
