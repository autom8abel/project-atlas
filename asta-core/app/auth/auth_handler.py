from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_db_connection
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# Read configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This tells FastAPI that the tokenUrl is the endpoint for login (which I will create next)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    """Verifies a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hashes a plain text password. (We already have this in routes/user.py, we can refactor later)"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a new JWT access token.
    The 'data' dict should contain the claims (e.g., user identifier).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), conn=Depends(get_db_connection)):
    """
    FastAPI Dependency that will be used to protect routes.
    It:
    1. Extracts the JWT from the Authorization header.
    2. Verifies the JWT is valid and not expired.
    3. Extracts the user identity from the JWT.
    4. Fetches the user from the database.
    5. Returns the user object.

    If any step fails, it raises an HTTPException.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode and verify the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch the user from the database
    query = "SELECT id, email, full_name, company_name, is_active, is_superuser, created_at FROM users WHERE id = $1"
    user = await conn.fetchrow(query, int(user_id))

    if user is None:
        raise credentials_exception
    return user