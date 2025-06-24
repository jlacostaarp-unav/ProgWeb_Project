from fastapi import APIRouter, HTTPException
from app.data.db import get_session
from app.models import Event
from app.models.registration import Registration
from sqlmodel import select


router = APIRouter()



@router.delete("/events/{event_id}")
def delete_event(event_id: int):
    session = next(get_session()) # you enter, "take control", of the session for making some changes or calling APIs.

    event = session.get(Event, event_id) # searches in the session if it has an event with that ID for deleting it.
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Deletes firstly the registrations that event can have.
    statement = select(Registration).where(Registration.event_id == event_id)
    registrations = session.exec(statement).all()
    for registration in registrations:
            session.delete(registration)

    session.delete(event) # eliminates the event from the session.
    session.commit() # "saves" changes.

    return {"message": f"Event {event_id} and {len(registrations)} registrations deleted successfully"}

@router.delete("/events")
def delete_all_events():
    session = next(get_session())

    try:
        # deletes the registrations of the event
        registrations = session.exec(select(Registration)).all()
        for registration in registrations:
            session.delete(registration)

        # deletes all events
        events = session.exec(select(Event)).all()
        for event in events:
            session.delete(event)

        session.commit()
        return {"message": f"{len(events)} events and {len(registrations)} registrations deleted successfully"}
    except Exception as e:
        session.rollback() # If we encounter an error, this function undoes all the changes (deletes) done.
        raise HTTPException(status_code=500, detail=str(e))