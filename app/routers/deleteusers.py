from fastapi import APIRouter, HTTPException
from app.data.db import get_session
from app.models.user import User
from app.models.registration import Registration
from sqlmodel import select


router = APIRouter()

@router.delete("/users/{username}")
def delete_user(username: str):
    session = next(get_session())

    user = session.get(User, username) # checks if the user exists.
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Deletes firstly the registrations that user can have.
    statement = select(Registration).where(Registration.username == username)
    registrations = session.exec(statement).all()
    for registration in registrations:
        session.delete(registration)

    # Then, the user is deleted.
    session.delete(user)
    session.commit()

    return {"message": f"User '{username}' and his registrations have been deleted successfully"}

@router.delete("/users")
def delete_all_users():
    session = next(get_session())

    try:
        # Obtain the registrations and users
        registrations = session.exec(select(Registration)).all()
        users = session.exec(select(User)).all()

        # First delete registrations of all users
        for registration in registrations:
            session.delete(registration)

        # Then, delete users
        for user in users:
            session.delete(user)

        session.commit()

        return {
            "message": f"{len(users)} users and {len(registrations)} registrations deleted successfully"
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))