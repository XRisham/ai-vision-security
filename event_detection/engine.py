import json
from .abandoned_object import detect_abandoned_object
from .crowd import detect_crowd
from .loitering import detect_loitering
from .restricted_zone import detect_restricted_zone
from tracking.track import Track


class EventEngine:
    def __init__(self, loitering_threshold: float, crowd_threshold: int, abandoned_threshold: float, zone_name: str, zone_points: str):
        self.loitering_threshold, self.crowd_threshold, self.abandoned_threshold = loitering_threshold, crowd_threshold, abandoned_threshold
        self.zone_name = zone_name
        try: self.zone = json.loads(zone_points)
        except json.JSONDecodeError: self.zone = []
        self.emitted: set[tuple[str, int | None]] = set()

    def evaluate(self, tracks: list[Track]) -> list[dict]:
        candidates = [detect_crowd(tracks, self.crowd_threshold)]
        for track in tracks:
            if track.missed_frames == 0:
                candidates += [detect_loitering(track, self.loitering_threshold), detect_restricted_zone(track, self.zone, self.zone_name), detect_abandoned_object(track, self.abandoned_threshold)]
        events = []
        for event in candidates:
            if event and (event["event_type"], event["track_id"]) not in self.emitted:
                self.emitted.add((event["event_type"], event["track_id"])); events.append(event)
        return events
