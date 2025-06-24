from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.registration import Registration
from app.models.event import Event
from app.models.user import User
from app.data.db import get_session
from pydantic import BaseModel

router = APIRouter()

class RegistrationRequest(BaseModel):
    username: str
    name: str
    email: str

@router.post("/events/{event_id}/register")
def register_user_to_event(event_id: int, registration: RegistrationRequest):
    session = next(get_session())

    # 1. Check if the event exists.
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 2. Check if user exists (if not create it).
    user = session.get(User, registration.username)
    if not user:
        user = User(username=registration.username, name=registration.name, email=registration.email)
        session.add(user)
        session.commit()
        session.refresh(user)

    # 3. Check if that registration already exists (avoid duplicated data).
    statement = select(Registration).where(
        Registration.username == registration.username,
        Registration.event_id == event_id
    )
    existing_registration = session.exec(statement).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail="User already registered for this event")

    # 4. Creates the registration.
    registration_entry = Registration(username=registration.username, event_id=event_id)
    session.add(registration_entry)
    session.commit()

    return {"message": f"User '{registration.username}' registered for event '{event.title}' successfully."}
