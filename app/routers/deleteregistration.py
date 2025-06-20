from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.models.registration import Registration
from app.data.db import get_session

router = APIRouter()


@router.delete("/registrations")
def delete_registration(username: str = Query(...), event_id: int = Query(...)):
    session = next(get_session())

    # Deletes a registration by name (button on the web).
    statement = select(Registration).where(
        Registration.username == username,
        Registration.event_id == event_id
    )
    registration = session.exec(statement).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()

    return {"message": f"Registration of user '{username}' for event '{event_id}' deleted successfully."}
