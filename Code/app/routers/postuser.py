from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.data.db import get_session
from app.models.user import User
from pydantic import BaseModel


router = APIRouter( #I had some problems for seeing this POST on /docs. I searched on the internet and discovered,
    # I had to implement this lines of code for not having that error.
    prefix="/users",
    tags=["Users"]  # This makes it visible in /docs
)

class UserCreate(BaseModel):
    username: str
    name: str
    email: str

@router.post("", response_model=User)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.get(User, user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(
        username=user_in.username,
        name=user_in.name,
        email=user_in.email
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
