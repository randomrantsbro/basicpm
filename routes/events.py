from fastapi import APIRouter, HTTPException
from ..models import Event
from ..database import db
from typing import List

router = APIRouter()


@router.post("/events/{user_id}", response_model=Event)
def create_event(user_id: int, event: Event):
    # Check if user exists
    user = db.table('users').get(doc_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    # Generate event id
    event_id = len(db.table('events')) + 1
    event.id = event_id
    event.user_id = user_id  # Associate event with user
    db.table('events').insert(event.dict())

    return event

@router.get("/events/{user_id}", response_model=List[Event])
def get_events(user_id: int):
    user = db.table('users').get(doc_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    events = [event for event in db.table('events').all() if event['user_id'] == user_id]
    return events

@router.get("/events/{user_id}/{event_id}", response_model=Event)
def get_event(user_id: int, event_id: int):
    event = db.table('events').get(doc_id=event_id)
    user = db.table('users').get(doc_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    if event['user_id'] != user_id:
        raise HTTPException(status_code=404, detail="Event not found for this user")
    return event

@router.put("/events/{user_id}/{event_id}", response_model=Event)
def update_event(user_id: int, event_id: int, event: Event):
    existing_event = db.table('events').get(doc_id=event_id)
    user = db.table('users').get(doc_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    if existing_event['user_id'] != user_id:
        raise HTTPException(status_code=404, detail="Event not found for this user")

    db.table('events').update(event.dict(), doc_ids=[event_id])
    return event

@router.delete("/events/{user_id}/{event_id}")
def delete_event(user_id: int, event_id: int):
    existing_event = db.table('events').get(doc_id=event_id)
    user = db.table('users').get(doc_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    if existing_event['user_id'] != user_id:
        raise HTTPException(status_code=404, detail="Event not found for this user")

    db.table('events').remove(doc_ids=[event_id])
    return {"message": "Event deleted"}
