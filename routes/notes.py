from fastapi import APIRouter, HTTPException
from ..models import Note
from ..database import db
from typing import List

router = APIRouter()

def user_exists(user_id: int):
    return db.table('users').get(doc_id=user_id) is not None

@router.post("/notes/{user_id}", response_model=Note)
def create_note(user_id: int, note: Note):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    note_id = len(db.table('notes')) + 1
    note.id = note_id
    note.user_id = user_id  # Associate note with user
    db.table('notes').insert(note.dict())
    return note

@router.get("/notes/{user_id}", response_model=List[Note])
def get_notes(user_id: int):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    notes = [note for note in db.table('notes').all() if note.get('user_id') == user_id]
    return notes

@router.get("/notes/{user_id}/{note_id}", response_model=Note)
def get_note(user_id: int, note_id: int):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    note = db.table('notes').get(doc_id=note_id)
    if note is None or note.get('user_id') != user_id:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found for user with id {user_id}")

    return note

@router.put("/notes/{user_id}/{note_id}", response_model=Note)
def update_note(user_id: int, note_id: int, note: Note):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    existing_note = db.table('notes').get(doc_id=note_id)
    if existing_note is None or existing_note.get('user_id') != user_id:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found for user with id {user_id}")

    db.table('notes').update(note.dict(), doc_ids=[note_id])
    return note

@router.delete("/notes/{user_id}/{note_id}")
def delete_note(user_id: int, note_id: int):
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    existing_note = db.table('notes').get(doc_id=note_id)
    if existing_note is None or existing_note.get('user_id') != user_id:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found for user with id {user_id}")

    db.table('notes').remove(doc_ids=[note_id])
    return {"message": "Note deleted"}