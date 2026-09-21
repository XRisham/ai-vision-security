from tracking.track import Track


def detect_crowd(tracks: list[Track], threshold: int) -> dict | None:
    count = sum(t.class_name == "person" and t.missed_frames == 0 for t in tracks)
    if count > threshold:
        return {"event_type":"crowd", "severity":"MEDIUM", "message":f"Crowd threshold exceeded: {count} people", "track_id":None, "confidence":None, "zone":None, "metadata_json":{"people_count":count}}
    return None
