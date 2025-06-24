from fastapi import APIRouter
from sqlmodel import select
from app.models.registration import Registration
from app.data.db import get_session

router = APIRouter()

@router.get("/registrations")
def get_registrations():
    session = next(get_session())
    statement = select(Registration)
    registrations = session.exec(statement).all()

    return [{"username": r.username, "event_id": r.event_id} for r in registrations]
