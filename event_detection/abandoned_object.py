from tracking.track import Track

EXCLUDED = {"person", "car", "bicycle", "motorcycle", "bus", "truck"}


def detect_abandoned_object(track: Track, threshold: float, movement_px: float = 20) -> dict | None:
    if track.class_name in EXCLUDED or track.duration_seconds < threshold or len(track.positions) < 2: return None
    a, b = track.positions[0], track.positions[-1]
    if ((a[0]-b[0])**2+(a[1]-b[1])**2)**.5 <= movement_px:
        return {"event_type":"abandoned_object", "severity":"LOW", "message":f"Stationary {track.class_name} may be abandoned", "track_id":track.id, "confidence":track.confidence, "zone":None, "metadata_json":{"bbox":track.bbox, "heuristic":True}}
    return None
