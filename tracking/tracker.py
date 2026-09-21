"""Lightweight persistent centroid tracker, compatible with YOLO detections.

For production crowded scenes use Ultralytics' configured ByteTrack tracker; this
dependency-free tracker keeps the local application usable without a tracker file.
"""
from datetime import datetime
from detection.detector import DetectionResult
from .track import Track


class CentroidTracker:
    def __init__(self, max_distance: float = 80, max_missed: int = 20):
        self.max_distance, self.max_missed = max_distance, max_missed
        self.tracks: dict[int, Track] = {}; self.next_id = 1

    @staticmethod
    def _center(bbox: list[float]) -> tuple[float, float]:
        return ((bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2)

    def update(self, detections: list[DetectionResult], now: datetime | None = None) -> list[Track]:
        now = now or datetime.utcnow()
        unmatched = set(range(len(detections)))
        matched: set[int] = set()
        candidates = []
        for tid, track in self.tracks.items():
            for index, detection in enumerate(detections):
                if track.class_name != detection.class_name: continue
                a, b = track.center, self._center(detection.bbox)
                candidates.append((((a[0]-b[0])**2+(a[1]-b[1])**2)**.5, tid, index))
        for distance, tid, index in sorted(candidates):
            if distance > self.max_distance or tid in matched or index not in unmatched: continue
            track, detection = self.tracks[tid], detections[index]
            track.bbox, track.confidence, track.last_seen = detection.bbox, detection.confidence, now
            track.positions.append(track.center); track.positions = track.positions[-120:]
            track.missed_frames = 0; matched.add(tid); unmatched.remove(index)
        for tid, track in list(self.tracks.items()):
            if tid not in matched:
                track.missed_frames += 1
                if track.missed_frames > self.max_missed: del self.tracks[tid]
        for index in unmatched:
            d = detections[index]; track = Track(self.next_id, d.class_name, d.confidence, d.bbox, now, now)
            track.positions.append(track.center); self.tracks[self.next_id] = track; self.next_id += 1
        return list(self.tracks.values())
