from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.database.schemas import CameraStart
from backend.services.live import processor
router=APIRouter(prefix="/cameras",tags=["cameras"])
@router.get("")
def cameras(): return [processor.snapshot()]
@router.post("/start")
def start_camera(body:CameraStart): processor.start(body.source); return processor.snapshot()
@router.post("/stop")
def stop_camera(): processor.stop(); return processor.snapshot()
@router.get("/stream")
def stream():
 if not processor.active and not processor.frame: raise HTTPException(409,"Camera is not running")
 return StreamingResponse(processor.mjpeg(),media_type="multipart/x-mixed-replace; boundary=frame")
