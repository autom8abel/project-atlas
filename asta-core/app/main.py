from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import engine
from app.db.base import Base  # <-- ADD THIS IMPORT
from app.routes import auth, user, task, faq

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create all database tables based on SQLAlchemy models
    print("Creating database tables if they don't exist...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables verified/created!")
    
    yield  # The application runs here
    
    # Shutdown: Close the database engine
    await engine.dispose()

# Create the FastAPI application instance
app = FastAPI(
    title="Project Atlas - ASTA Core API",
    description="The core API for the ASTA AI Assistant", 
    version="0.1.0",
    lifespan=lifespan
)

# Include the routers
app.include_router(auth.router)
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
app.include_router(faq.router, prefix="/faq", tags=["FAQ"])

# A simple root endpoint to test if the API is running
@app.get("/")
async def root():
    return {"message": "Welcome to the ASTA Core API"}
