from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import engine
from app.routes import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: We can add code here to create DB tables if needed later
    # For now, we'll just pass. Our tables are already created by our SQL script
    yield
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

# A simple root endpoint to test if the API is running
@app.get("/")
async def root():
    return {"message": "Welcome to the ASTA Core API"}
