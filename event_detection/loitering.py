from tracking.track import Track


def detect_loitering(track: Track, threshold: float) -> dict | None:
    if track.class_name == "person" and track.duration_seconds >= threshold:
        return {"event_type":"loitering", "severity":"MEDIUM", "message":"Person detected loitering in monitored area", "track_id":track.id, "confidence":track.confidence, "zone":None, "metadata_json":{"bbox":track.bbox}}
    return None
