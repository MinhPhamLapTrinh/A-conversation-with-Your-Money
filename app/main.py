from typing import Union, Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.db import init_db
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting application in {settings.APP_ENV} environment...")
    try:
        await init_db()
        print("Database connection initialized successfully.")
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
    yield

app = FastAPI(title="A conversation with your Money", 
              description="Understand why you spend, not HOW MUCH", 
              version="1.0.0",
              lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

