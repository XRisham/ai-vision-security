import logging
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class DetectionResult:
    class_name: str
    confidence: float
    bbox: list[float]


class YOLODetector:
    def __init__(self, model_name: str):
        self.model = None
        self.model_name = model_name

    def load(self) -> None:
        try:
            from ultralytics import YOLO
            self.model = YOLO(self.model_name)
        except Exception as exc:
            logger.error("Could not load YOLO model '%s': %s", self.model_name, exc)
            raise RuntimeError(f"Could not load YOLO model '{self.model_name}': {exc}") from exc

    def detect(self, frame: np.ndarray) -> list[DetectionResult]:
        if self.model is None: self.load()
        result = self.model(frame, verbose=False)[0]
        names = result.names
        return [DetectionResult(str(names[int(box.cls[0])]), float(box.conf[0]), [float(x) for x in box.xyxy[0].tolist()]) for box in result.boxes]
