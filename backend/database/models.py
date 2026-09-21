from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Detection(Base):
    __tablename__ = "detections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    track_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    class_name: Mapped[str] = mapped_column(String(80), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    bbox: Mapped[list] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    severity: Mapped[str] = mapped_column(String(20), index=True)
    message: Mapped[str] = mapped_column(Text)
    track_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    zone: Mapped[str | None] = mapped_column(String(120), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class Camera(Base):
    __tablename__ = "cameras"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), default="Default camera")
    source: Mapped[str] = mapped_column(String(500), default="0")
    active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Configuration(Base):
    __tablename__ = "configuration"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    value: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
