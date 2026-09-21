from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from backend.database.models import Detection
from backend.database.schemas import DetectionOut
router=APIRouter(prefix="/detections",tags=["detections"])
def db_session():
 db=SessionLocal()
 try: yield db
 finally: db.close()
@router.get("",response_model=list[DetectionOut])
def detections(skip:int=0,limit:int=Query(50,le=200),db:Session=Depends(db_session)):
 return list(db.scalars(select(Detection).order_by(Detection.timestamp.desc()).offset(skip).limit(limit)))
