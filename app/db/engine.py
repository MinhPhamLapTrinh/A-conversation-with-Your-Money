from sqlmodel import create_engine
from app.config import settings

# Create an Engine to hold the connection to the database
engine = create_engine(settings.POSTGRES_URL, echo=True)
