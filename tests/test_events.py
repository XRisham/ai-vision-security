from datetime import datetime, timedelta
from event_detection.crowd import detect_crowd
from event_detection.loitering import detect_loitering
from event_detection.restricted_zone import detect_restricted_zone
from tracking.track import Track

def track(id=1, cls="person", seconds=0, point=(5,5)):
 now=datetime.utcnow(); return Track(id,cls,.9,[point[0]-1,point[1]-1,point[0]+1,point[1]+1],now-timedelta(seconds=seconds),now,[point])
def test_loitering(): assert detect_loitering(track(seconds=31),30)["severity"] == "MEDIUM"
def test_crowd(): assert detect_crowd([track(i) for i in range(6)],5)["event_type"] == "crowd"
def test_restricted_zone(): assert detect_restricted_zone(track(point=(5,5)),[[0,0],[10,0],[10,10],[0,10]],"Zone A")["zone"] == "Zone A"
