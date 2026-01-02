from sqlmodel import SQLModel
from app.db.engine import engine

# Force db models to be imported
import app.models.db.models


async def init_db():
    SQLModel.metadata.create_all(engine)
