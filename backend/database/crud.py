from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Configuration, Detection, Event


def list_events(db: Session, skip: int = 0, limit: int = 50, severity: str | None = None, event_type: str | None = None):
    query = select(Event).order_by(Event.timestamp.desc()).offset(skip).limit(limit)
    if severity: query = query.where(Event.severity == severity.upper())
    if event_type: query = query.where(Event.event_type == event_type)
    return list(db.scalars(query))


def save_event(db: Session, payload: dict) -> Event:
    item = Event(**payload); db.add(item); db.commit(); db.refresh(item); return item


def get_or_default(db: Session, key: str, default: str) -> str:
    item = db.scalar(select(Configuration).where(Configuration.key == key)); return item.value if item else default


def set_value(db: Session, key: str, value: str) -> None:
    item = db.scalar(select(Configuration).where(Configuration.key == key))
    if item: item.value = value
    else: db.add(Configuration(key=key, value=value))
    db.commit()
