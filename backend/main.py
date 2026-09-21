import asyncio, logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.database.database import init_db, SessionLocal
from backend.database.models import Event
from sqlalchemy import func, select
from backend.api.routes import health, events, detections, cameras, settings as settings_route
from backend.services.live import processor

logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(); yield; processor.stop()

app=FastAPI(title=settings.app_name,version="0.1.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["*"],allow_headers=["*"])
for router in (health.router,events.router,detections.router,cameras.router,settings_route.router): app.include_router(router,prefix="/api")

@app.get("/api/statistics")
def statistics():
    db=SessionLocal()
    try:
        event_count=db.scalar(select(func.count(Event.id))) or 0
        by_type=dict(db.execute(select(Event.event_type,func.count(Event.id)).group_by(Event.event_type)).all())
        return {**processor.snapshot(),"event_count":event_count,"event_types":by_type}
    finally: db.close()

@app.websocket("/ws/live")
async def live_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(processor.snapshot())
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
