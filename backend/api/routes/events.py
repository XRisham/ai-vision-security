from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from backend.database.models import Event
from backend.database.schemas import EventOut
from backend.database.crud import list_events
router = APIRouter(prefix="/events", tags=["events"])
def db_session():
    db=SessionLocal()
    try: yield db
    finally: db.close()
@router.get("", response_model=list[EventOut])
def events(skip:int=0, limit:int=Query(50,le=200), severity:str|None=None, event_type:str|None=None, db:Session=Depends(db_session)): return list_events(db,skip,limit,severity,event_type)
@router.get("/{event_id}", response_model=EventOut)
def event(event_id:int, db:Session=Depends(db_session)):
    item=db.get(Event,event_id)
    if not item: raise HTTPException(404,"Event not found")
    return item
@router.delete("/{event_id}", status_code=204)
def delete_event(event_id:int, db:Session=Depends(db_session)):
    item=db.get(Event,event_id)
    if not item: raise HTTPException(404,"Event not found")
    db.delete(item); db.commit()
