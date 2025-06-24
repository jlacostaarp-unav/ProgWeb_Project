from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.data.db import engine
from app.models import Event

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/events", response_model=List[Event])
def read_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()

@router.get("/events/{event_id}")
def get_event(event_id: int):
    session = next(get_session())
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event