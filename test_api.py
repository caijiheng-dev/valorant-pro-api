from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_teams():
    r = client.get("/api/players/teams")
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == 200
    assert len(data["data"]) > 0


def test_player_list():
    r = client.get("/api/players/list?page=1&pageSize=10")
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == 200
    assert data["data"]["total"] > 0
