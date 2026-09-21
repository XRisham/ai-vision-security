from tracking.track import Track


def point_in_polygon(point: tuple[float, float], polygon: list[list[float]]) -> bool:
    if len(polygon) < 3: return False
    x, y = point; inside = False; j = len(polygon)-1
    for i, (xi, yi) in enumerate(polygon):
        xj, yj = polygon[j]
        if (yi > y) != (yj > y) and x < (xj-xi)*(y-yi)/(yj-yi or 1e-12)+xi: inside = not inside
        j = i
    return inside


def detect_restricted_zone(track: Track, polygon: list[list[float]], name: str) -> dict | None:
    if track.class_name == "person" and point_in_polygon(track.center, polygon):
        return {"event_type":"restricted_zone_entry", "severity":"HIGH", "message":f"Person entered {name}", "track_id":track.id, "confidence":track.confidence, "zone":name, "metadata_json":{"bbox":track.bbox}}
    return None
