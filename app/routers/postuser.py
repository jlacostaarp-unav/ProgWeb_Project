from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.data.db import get_session
from app.models.user import User

router = APIRouter( #I had some problems for seeing this POST on /docs. I searched on the internet and discovered,
    # I had to implement this lines of code for not having that error.
    prefix="/users",
    tags=["Users"]  # This makes it visible in /docs
)


@router.post("", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    existing_user = session.get(User, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
