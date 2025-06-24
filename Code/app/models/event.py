from sqlmodel import SQLModel, Field
from datetime import datetime

#I created this file to define the Class Event that will save the data of each event.

class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str
