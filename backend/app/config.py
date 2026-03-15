from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    secret_key: str = "cdungeon-super-secret-key-change-in-prod"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    database_url: str = f"sqlite:///{BASE_DIR}/dungeon.db"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    share_cache_dir: Path = BASE_DIR / "share_cache"

    class Config:
        env_file = ".env"


settings = Settings()
settings.share_cache_dir.mkdir(exist_ok=True)
