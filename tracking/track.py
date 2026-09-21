from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Track:
    id: int
    class_name: str
    confidence: float
    bbox: list[float]
    first_seen: datetime
    last_seen: datetime
    positions: list[tuple[float, float]] = field(default_factory=list)
    missed_frames: int = 0

    @property
    def center(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.bbox; return ((x1+x2)/2, (y1+y2)/2)

    @property
    def duration_seconds(self) -> float:
        return (self.last_seen - self.first_seen).total_seconds()
