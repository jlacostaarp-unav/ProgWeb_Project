from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlmodel import Session
from app.data.db import get_session
from app.models import Event

router = APIRouter()

class EventIn(BaseModel):
    title: str
    description: str
    date: datetime
    location: str

@router.post("/events", response_model=Event)
def create_event(event_in: EventIn, session: Session = Depends(get_session)):
    event = Event(
        title=event_in.title,
        description=event_in.description,
        date=event_in.date,
        location=event_in.location
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
