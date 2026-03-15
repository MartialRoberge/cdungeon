from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    stats = relationship("PlayerStats", back_populates="player", uselist=False, cascade="all, delete-orphan")
    room_completions = relationship("RoomCompletion", back_populates="player", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="player", cascade="all, delete-orphan")
    concept_accuracy = relationship("ConceptAccuracy", back_populates="player", cascade="all, delete-orphan")
    badges = relationship("PlayerBadge", back_populates="player", cascade="all, delete-orphan")
    daily_completions = relationship("DailyCompletion", back_populates="player", cascade="all, delete-orphan")


class PlayerStats(Base):
    __tablename__ = "player_stats"
    player_id = Column(Integer, ForeignKey("players.id"), primary_key=True)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    total_attempts = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    best_combo = Column(Integer, default=0)
    current_zone = Column(Integer, default=1)
    daily_streak = Column(Integer, default=0)
    last_daily_date = Column(String, default=None)

    player = relationship("Player", back_populates="stats")


class RoomCompletion(Base):
    __tablename__ = "room_completions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    room_id = Column(String, nullable=False)
    zone_number = Column(Integer, nullable=False)
    room_number = Column(Integer, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    attempts_taken = Column(Integer, nullable=False)
    xp_earned = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("player_id", "room_id"),)
    player = relationship("Player", back_populates="room_completions")


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    challenge_id = Column(String, nullable=False)
    concept_tags = Column(Text, nullable=False)  # JSON array string
    correct = Column(Boolean, nullable=False)
    time_ms = Column(Integer)
    combo_at_time = Column(Integer, default=1)
    attempted_at = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="attempts")


class ConceptAccuracy(Base):
    __tablename__ = "concept_accuracy"
    player_id = Column(Integer, ForeignKey("players.id"), primary_key=True)
    concept_tag = Column(String, primary_key=True)
    total = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    player = relationship("Player", back_populates="concept_accuracy")


class Badge(Base):
    __tablename__ = "badges"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon_key = Column(String, nullable=False)
    category = Column(String, nullable=False)
    secret = Column(Boolean, default=False)

    player_badges = relationship("PlayerBadge", back_populates="badge")


class PlayerBadge(Base):
    __tablename__ = "player_badges"
    player_id = Column(Integer, ForeignKey("players.id"), primary_key=True)
    badge_id = Column(String, ForeignKey("badges.id"), primary_key=True)
    earned_at = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="badges")
    badge = relationship("Badge", back_populates="player_badges")


class DailyCompletion(Base):
    __tablename__ = "daily_completions"
    player_id = Column(Integer, ForeignKey("players.id"), primary_key=True)
    date = Column(String, primary_key=True)
    completed_at = Column(DateTime, default=datetime.utcnow)
    xp_earned = Column(Integer, nullable=False)

    player = relationship("Player", back_populates="daily_completions")
