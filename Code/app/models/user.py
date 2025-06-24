from sqlmodel import SQLModel, Field

#I created this file to define the Class User that will save the data of each User.

class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    name: str
    email: str