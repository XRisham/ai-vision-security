import cv2


def normalize_frame(frame):
    """Ensure a BGR frame is contiguous for OpenCV/YOLO."""
    return cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), cv2.COLOR_RGB2BGR)
