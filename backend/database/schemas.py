from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; event_type: str; severity: str; message: str; track_id: int | None
    confidence: float | None; zone: str | None; metadata_json: dict | None; timestamp: datetime


class DetectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; track_id: int | None; class_name: str; confidence: float; bbox: list; timestamp: datetime


class CameraStart(BaseModel):
    source: str = Field(default="0", min_length=1)
    name: str = "Default camera"


class CameraOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; name: str; source: str; active: bool; created_at: datetime


class SettingsUpdate(BaseModel):
    loitering_threshold: float | None = Field(default=None, gt=0)
    crowd_threshold: int | None = Field(default=None, gt=0)
    abandoned_object_threshold: float | None = Field(default=None, gt=0)
    restricted_zone_name: str | None = None
    restricted_zone_points: list[list[float]] | None = None
