from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Vision Security"
    debug: bool = True
    database_url: str = "sqlite:///./ai_vision.db"
    yolo_model: str = "yolo11n.pt"
    camera_source: str = "0"
    loitering_threshold: float = 30.0
    crowd_threshold: int = 5
    abandoned_object_threshold: float = 30.0
    host: str = "0.0.0.0"
    port: int = 8000
    restricted_zone_name: str = "Restricted Area"
    restricted_zone_points: str = "[]"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
