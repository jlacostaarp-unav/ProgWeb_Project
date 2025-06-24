from sqlmodel import SQLModel, Field

# From the other two classes: Event and User, in this new class, Registration, I combine them so that a user can
# registrate to an event. I make a class with username and event_id, which will be the data shown in JSON when
# you do a GET request of registrations.

class Registration(SQLModel, table=True):
    username: str = Field(primary_key=True, foreign_key="user.username")
    event_id: int = Field(primary_key=True, foreign_key="event.id")
