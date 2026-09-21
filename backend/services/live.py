import asyncio, logging, threading, time
from datetime import datetime
import cv2
from backend.config.settings import settings
from backend.database.database import SessionLocal
from backend.database.models import Detection
from backend.database.crud import save_event
from detection.detector import YOLODetector
from tracking.tracker import CentroidTracker
from event_detection.engine import EventEngine

logger = logging.getLogger(__name__)


class LiveProcessor:
    def __init__(self):
        self.active = False; self.thread: threading.Thread | None = None; self.frame: bytes | None = None
        self.error: str | None = None; self.source = settings.camera_source; self.fps = 0.0; self.tracks = []
        self.events: list[dict] = []; self._lock = threading.Lock()

    def start(self, source: str) -> None:
        if self.active: self.stop()
        self.source, self.error, self.active = source, None, True
        self.thread = threading.Thread(target=self._run, daemon=True); self.thread.start()

    def stop(self) -> None:
        self.active = False
        if self.thread: self.thread.join(timeout=3)

    def _run(self) -> None:
        raw_source = int(self.source) if self.source.isdigit() else self.source
        cap = cv2.VideoCapture(raw_source)
        if not cap.isOpened(): self.error = f"Unable to open camera/video source: {self.source}"; self.active = False; return
        tracker = CentroidTracker(); engine = EventEngine(settings.loitering_threshold, settings.crowd_threshold, settings.abandoned_object_threshold, settings.restricted_zone_name, settings.restricted_zone_points)
        try:
            detector = YOLODetector(settings.yolo_model); detector.load()
        except RuntimeError as exc:
            self.error = str(exc); self.active = False; cap.release(); return
        previous = time.monotonic()
        while self.active:
            ok, frame = cap.read()
            if not ok: self.error = "Video source ended or frame could not be read"; self.active = False; break
            detections = detector.detect(frame); now = datetime.utcnow(); self.tracks = tracker.update(detections, now)
            events = engine.evaluate(self.tracks)
            db = SessionLocal()
            try:
                for detection in detections: db.add(Detection(class_name=detection.class_name, confidence=detection.confidence, bbox=detection.bbox, timestamp=now))
                for event in events: save_event(db, event)
            except Exception as exc: db.rollback(); logger.exception("Could not persist processing results: %s", exc)
            finally: db.close()
            with self._lock: self.events.extend(events); self.events = self.events[-50:]
            for track in self.tracks:
                if track.missed_frames == 0:
                    x1,y1,x2,y2 = map(int, track.bbox); cv2.rectangle(frame,(x1,y1),(x2,y2),(0,220,130),2)
                    cv2.putText(frame,f"{track.class_name} #{track.id} {track.confidence:.2f}",(x1,max(18,y1-7)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,220,130),2)
            current = time.monotonic(); self.fps = 1/max(current-previous, .001); previous = current
            cv2.putText(frame,f"FPS {self.fps:.1f}",(10,28),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2)
            ok, buffer = cv2.imencode(".jpg", frame)
            if ok:
                with self._lock: self.frame = buffer.tobytes()
        cap.release()

    def snapshot(self) -> dict:
        visible = [t for t in self.tracks if t.missed_frames == 0]
        return {"camera_active":self.active,"source":self.source,"error":self.error,"fps":round(self.fps,1),"people_count":sum(t.class_name=="person" for t in visible),"object_count":len(visible),"tracks":[{"track_id":t.id,"class_name":t.class_name,"confidence":t.confidence,"bbox":t.bbox,"duration_seconds":round(t.duration_seconds,1)} for t in visible],"events":self.events[-10:]}

    def mjpeg(self):
        while self.active or self.frame:
            with self._lock: frame = self.frame
            if frame: yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            time.sleep(.06)


processor = LiveProcessor()
