import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from backend.database.crud import get_or_default, set_value
from backend.database.schemas import SettingsUpdate
from backend.config.settings import settings
router=APIRouter(prefix="/settings",tags=["settings"])
def db_session():
 db=SessionLocal()
 try: yield db
 finally: db.close()
def values(db):
 return {"loitering_threshold":float(get_or_default(db,"loitering_threshold",str(settings.loitering_threshold))),"crowd_threshold":int(get_or_default(db,"crowd_threshold",str(settings.crowd_threshold))),"abandoned_object_threshold":float(get_or_default(db,"abandoned_object_threshold",str(settings.abandoned_object_threshold))),"restricted_zone_name":get_or_default(db,"restricted_zone_name",settings.restricted_zone_name),"restricted_zone_points":json.loads(get_or_default(db,"restricted_zone_points",settings.restricted_zone_points))}
@router.get("")
def get_settings(db:Session=Depends(db_session)): return values(db)
@router.put("")
def update_settings(body:SettingsUpdate,db:Session=Depends(db_session)):
 for key,value in body.model_dump(exclude_none=True).items(): set_value(db,key,json.dumps(value) if key=="restricted_zone_points" else str(value))
 return values(db)
