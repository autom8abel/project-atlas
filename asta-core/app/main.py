from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import create_db_pool

print("✅ main.py is starting to execute")  # DEBUG

# Import routers using the direct method
try:
    from app.routes.user import router as user_router
    print("✅ User router imported successfully")  # DEBUG
except ImportError as e:
    print(f"❌ Failed to import user_router: {e}")  # DEBUG

try:
    from app.routes.auth import router as auth_router
    print("✅ Auth router imported successfully")  # DEBUG
except ImportError as e:
    print(f"❌ Failed to import auth_router: {e}")  # DEBUG

# Lifespan events: Code to run on startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create the database connection pool
    await create_db_pool()
    yield
    # Shutdown: Close the pool (we'll add this later)
    # await close_db_pool()

# Create the FastAPI application instance, passing the lifespan manager
app = FastAPI(
    title="Project Atlas - ASTA Core API",
    description="The core API for the ASTA AI Assistant",
    version="0.1.0",
    lifespan=lifespan
)

print("✅ FastAPI app instance created")  # DEBUG

# Include the routers
try:
    app.include_router(auth_router)
    print("✅ Auth router included successfully")  # DEBUG
except NameError as e:
    print(f"❌ Failed to include auth_router (NameError): {e}")  # DEBUG
except Exception as e:
    print(f"❌ Failed to include auth_router: {e}")  # DEBUG

try:
    app.include_router(user_router, prefix="/users", tags=["users"])
    print("✅ User router included successfully")  # DEBUG
except NameError as e:
    print(f"❌ Failed to include user_router (NameError): {e}")  # DEBUG
except Exception as e:
    print(f"❌ Failed to include user_router: {e}")  # DEBUG

# A simple root endpoint to test if the API is running
@app.get("/")
async def root():
    return {"message": "Welcome to the ASTA Core API"}

print("✅ main.py finished execution")  # DEBUG