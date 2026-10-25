import logging
import os
from fastapi import FastAPI
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(mwssage)s",
    filename="app.log",
)
logger = logging.getLogger("notes")

app = FastAPI(title="Notes", version=APP_VERSION)

notes = {}
next_id = 1

logger.info("Notes service loaded, version=%s", APP_VERSION)

@app.get("/")
def root():
    return {"service":"notes"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.get("/notes")
def get_notes(sort: str = ""):
    items = list(notes.values())
    if sort == "priority":
        items = sorted(items, key=lambda n: n["priority"])
    elif sort == "-priority":
        items = sorted(items, key=lambda n: n["priority"], reverse=True)
    logger.info("Get notes, sort=%r count=%s", sort, len(items))
    return items

@app.post("/notes")
def create_note(data: dict):
    global next_id
    note = {
        "id": next_id,
        "title": data.get("title", ""),
        "text": data.get("text", ""),
        "priority": data.get("priority", 1),
    }
    notes[next_id] = note
    next_id += 1
    logger.info("Created note id=%s priority=%s", note["id"], note["priority"])
    return note

@app.get("/notes/{note_id}")
def get_note(note_id:int):
    if note_id not in notes:
        logger.warning("Note %s not found", note_id)
        return {"error": "Note not found"}
    logger.info("Get note id=%s", note_id)
    return notes[note_id]

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if note_id not in notes:
        loger.warning("Note %s not found", note_id)
        return {"error": "Note not found"}
    del notes[note_id]
    logger.info("Delete note id=%s", note_id)
    return {"ok": True}
