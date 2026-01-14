from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.db import init_db
from app.config import settings
from app.routes import auth, transaction, finance


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting application in {settings.APP_ENV} environment...")
    try:
        await init_db()
        print("Database connection initialized successfully.")
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
    yield


app = FastAPI(
    title="A conversation with your Money",
    description="Understand why you spend, not HOW MUCH",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API route
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(transaction.router, prefix="/api/v1", tags=["Transaction"])
app.include_router(finance.router, prefix="/api/v1/finance", tags=["Finance"])

# Root endpoint for health checks or basic info
@app.get("/")
async def root():
    return {"message": "Welcome to A conversation with Your Money!"}