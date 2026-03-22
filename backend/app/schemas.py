from pydantic import BaseModel, field_validator
from datetime import datetime


# --- Auth ---
class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3 or len(v) > 20:
            raise ValueError("Username must be 3-20 characters")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, _ and -")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v: str) -> str:
        if len(v) < 4:
            raise ValueError("Password must be at least 4 characters")
        return v


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    player_id: int
    username: str


# --- Player ---
class PlayerMe(BaseModel):
    id: int
    username: str
    xp: int
    level: int
    current_zone: int
    daily_streak: int
    best_combo: int
    total_attempts: int
    total_correct: int


class BadgeOut(BaseModel):
    id: str
    name: str
    description: str
    icon_key: str
    category: str
    secret: bool
    earned: bool
    earned_at: datetime | None = None


# --- Dungeon ---
class ZoneOut(BaseModel):
    zone_number: int
    name: str
    theme: str
    emoji: str
    rooms_total: int
    rooms_cleared: int
    is_unlocked: bool
    is_boss_cleared: bool
    boss_name: str
    has_mini_boss_1: bool
    has_mini_boss_2: bool


class RoomOut(BaseModel):
    room_id: str
    zone_number: int
    room_number: int
    name: str
    challenge_type: str
    is_boss: bool
    is_mini_boss: bool
    is_cleared: bool
    is_locked: bool
    attempts_taken: int


# --- Room attempt ---
class AttemptRequest(BaseModel):
    answer: str | int | list[str] | dict[str, str]
    combo: int = 1
    time_ms: int = 5000


class AttemptResponse(BaseModel):
    correct: bool
    explanation: str
    xp_earned: int
    new_total_xp: int
    new_level: int | None
    combo: int
    hint_scroll: str | None
    badge_unlocked: BadgeOut | None
    room_cleared: bool
    zone_cleared: bool
    is_mini_boss: bool


# --- Orb (placeholder for future AI orb) ---
class OrbContext(BaseModel):
    concept_tags: list[str]
    difficulty: int
    player_accuracy: dict[str, float]


class OrbHintRequest(BaseModel):
    room_id: str
    player_context: OrbContext


class OrbHintResponse(BaseModel):
    hint: str
    source: str = "static"


# --- Daily ---
class DailyOut(BaseModel):
    date: str
    challenge: dict[str, object]
    already_completed: bool
    xp_bonus: int
    streak_days: int
