from detection.detector import DetectionResult
from tracking.tracker import CentroidTracker
def test_persistent_id():
 t=CentroidTracker(); one=t.update([DetectionResult("person",.9,[0,0,10,10])])[0]
 two=t.update([DetectionResult("person",.8,[2,0,12,10])])[0]
 assert one.id == two.id and len(two.positions) == 2
