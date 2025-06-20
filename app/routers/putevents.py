from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.data.db import get_session
from app.models import Event

router = APIRouter()
# I created a class for requesting and saving data and then refreshing (updating) it into the original one.
class EventUpdate(BaseModel):
    title: str
    description: str
    date: datetime
    location: str
@router.put("/events/{event_id}")
def update_event(event_id: int, event_update: EventUpdate):
    session = next(get_session())
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = event_update.title
    event.description = event_update.description
    event.date = event_update.date
    event.location = event_update.location

    session.add(event)
    session.commit()
    session.refresh(event)
    return event
