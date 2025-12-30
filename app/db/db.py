from sqlmodel import SQLModel
from app.db.engine import engine


async def init_db():
    SQLModel.metadata.create_all(engine)
