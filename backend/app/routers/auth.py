from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Player, PlayerStats
from app.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(player_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": str(player_id), "exp": expire}, settings.secret_key, algorithm=settings.algorithm)


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(Player).filter(Player.username == data.username).first():
        raise HTTPException(status_code=400, detail="Ce pseudo est déjà pris !")
    player = Player(
        username=data.username,
        password_hash=pwd_context.hash(data.password),
    )
    db.add(player)
    db.flush()
    stats = PlayerStats(player_id=player.id)
    db.add(stats)
    db.commit()
    db.refresh(player)
    return TokenResponse(access_token=create_token(player.id), player_id=player.id, username=player.username)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.username == data.username).first()
    if not player or not pwd_context.verify(data.password, player.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Pseudo ou mot de passe incorrect")
    player.last_seen = datetime.utcnow()
    db.commit()
    return TokenResponse(access_token=create_token(player.id), player_id=player.id, username=player.username)
