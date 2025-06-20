from app.config import config

# NB: do not add imports here!

from pathlib import Path
import os

# ...and here!!

if Path(__file__).parent == Path(os.getcwd()):
    config.root_dir = "."
# You can add imports from here...
from fastapi import FastAPI

#All the calls to the /routers files which contains the different APIs.
from app.routers import frontend
from app.routers import getevents
from app.routers import postevents
from app.routers import deleteevent
from app.routers import putevents
from app.routers import postuserevents
from app.routers import getuser
from app.routers import postuser
from app.routers import deleteusers
from app.routers import getregistrations
from app.routers import deleteregistration


from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.data.db import init_database



#Creates an asyncronous context.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield
    # on close


#Creates a directory for static files
app = FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory=config.root_dir / "static"),
    name="static"
)

#Inclusion of all the APIs and the Frontend.
app.include_router(frontend.router) #Calls frontend
app.include_router(getevents.router) #Calls the API of GET event
app.include_router(postevents.router) #Calls the API of POST event
app.include_router(deleteevent.router) # Calls the API of DELETE event
app.include_router(putevents.router) # Calls the API of PUT event
app.include_router(postuserevents.router) # Calls the API of POST to register a user to an event
app.include_router(getuser.router) # Call the API of GET user
app.include_router(postuser.router) # Call the API of POST user
app.include_router(deleteusers.router) # Call the API of DELETE user
app.include_router(getregistrations.router) # Call the API of GET registrations
app.include_router(deleteregistration.router) # Call the API of DELETE registrations


# Uses univcorn to execute the FastAPI.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

