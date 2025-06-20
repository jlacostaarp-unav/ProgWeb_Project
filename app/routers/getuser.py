from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.data.db import get_session
from app.models.user import User

router = APIRouter()

@router.get("/users", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.get("/users/{username}")
def get_users(username: str):
    session = next(get_session())
    user = session.get(User, username) # Filters by username.
    if not user:
        raise HTTPException(status_code=404, detail="Event not found")
    return user
