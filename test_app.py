from fastapi.testclient import TestClient
from app_final import app, notes

client = TestClient(app)

def setup_function(_):
    notes.clear()

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_create_and_get_note():
    r = client.post("/notes", json={"title": "a", "text": "b", "priority": 3})
    assert r.status_code == 200
    note_id = r.json()["id"]
    assert r.json()["priority"] == 3
    r2 = client.get(f"/notes/{note_id}")
    assert r2.json()["title"] == "a"

def test_note_not_found():
    r = client.get("/notes/5")
    assert r.json() == {"error": "Note not found"}

def test_sort_by_priority():
    client.post("/notes", json={"title": "a", "priority": 3})
    client.post("/notes", json={"title": "b", "priority": 1})
    client.post("/notes", json={"title": "c", "priority": 5})
    r = client.get("/notes?sort=priority")
    assert [n["priority"] for n in r.json()] == [1, 3, 5]
    r2 = client.get("/notes?sort=-priority")
    assert [n["priority"] for n in r2.json()] == [5, 3, 1]
