import os
os.environ["DATABASE_URL"]="sqlite:///./test_ai_vision.db"
from fastapi.testclient import TestClient
from backend.main import app
def test_health():
 with TestClient(app) as client: assert client.get("/api/health").json()["status"] == "online"
def test_settings():
 with TestClient(app) as client:
  assert client.put("/api/settings",json={"crowd_threshold":7}).status_code == 200
  assert client.get("/api/settings").json()["crowd_threshold"] == 7
def test_events_empty():
 with TestClient(app) as client: assert client.get("/api/events").status_code == 200
