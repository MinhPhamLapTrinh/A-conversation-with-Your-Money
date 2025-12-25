from sqlmodel import Session
from app.db.engine import engine
from fastapi import Depends
from typing import Annotated
"""
A session is what stores the objs in memory and keeps track of any changes needed in the data, then it uses the engine to
communicate with the database
"""
def get_session():
    # Make this generator acted as a FastAPI dependency
    with Session(engine) as session:
        yield session # yield allows cleanup after request finishes

SessionDep = Annotated[Session, Depends(get_session)]