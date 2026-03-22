from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Badge
from app.content.badges_data import BADGES_SEED
from app.routers import auth, player, dungeon, rooms, share, leaderboard
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="C:\\DUNGEON API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(player.router)
app.include_router(dungeon.router)
app.include_router(rooms.router)
app.include_router(share.router)
app.include_router(leaderboard.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    # Seed badges
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        for b in BADGES_SEED:
            existing = db.query(Badge).filter_by(id=b["id"]).first()
            if not existing:
                db.add(Badge(**b))
        db.commit()
        logger.info(f"C:\\DUNGEON API started. {len(BADGES_SEED)} badges seeded.")
    finally:
        db.close()


@app.get("/")
def root():
    from app.content.challenge_types import ZONE_COUNT
    from app.content.challenges_data import CHALLENGES
    return {"message": "C:\\DUNGEON API", "status": "online", "zones": ZONE_COUNT, "challenges": len(CHALLENGES)}
