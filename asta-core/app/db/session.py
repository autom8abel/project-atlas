from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Read the database URL from environment variables
# Format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the async engine. This is the starting point of any SQLAlchemy application
engine = create_async_engine(
    DATABASE_URL,
    echo=True,   # Set to False in production
    future=True  # Use SQLAlchemy 2.0 API
)

# Create a configured "Session" class
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency function to get a database session
async def get_db():
    """
    Provides an async database session for a request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
