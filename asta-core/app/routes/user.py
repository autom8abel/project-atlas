from fastapi import APIRouter, HTTPException, Depends, status
import asyncpg
from app.schemas.user import User, UserCreate
from app.db.database import get_db_connection
from passlib.context import CryptContext
from app.auth.auth_handler import get_current_user

# Create a router for all /users endpoints
router = APIRouter()

# Set up password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt."""
    return pwd_context.hash(password)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, conn=Depends(get_db_connection)):
    """
    Create a new user.
    - Hash their password before storing it.
    - Insert the new user into the database.
    - Return the created user (without the password).
    """
    hashed_password = hash_password(user_data.password)

    try:
        # Execute the SQL query to insert the new user
        query = """
            INSERT INTO users (email, hashed_password, full_name, company_name)
            VALUES ($1, $2, $3, $4)
            RETURNING id, email, full_name, company_name, is_active, is_superuser, created_at
        """
        # conn.execute() returns the record that was inserted because of 'RETURNING'
        user_record = await conn.fetchrow(
            query, user_data.email, hashed_password, user_data.full_name, user_data.company_name
        )

    except asyncpg.exceptions.UniqueViolationError:
        # If the email already exists, postgres will raise this error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    # The returned record is an asyncpg Record object. We can convert it to a dict.
    return dict(user_record)

@router.get("/", response_model=list[User])
async def get_all_users(
    conn=Depends(get_db_connection),
    current_user: User = Depends(get_current_user) # <-- NEW DEPENDENCY
):
    """
    Get a list of all users.
    **Requires authentication.**
    """
    # You could also add authorization here later, e.g.:
    # if not current_user.is_superuser:
    #    raise HTTPException(status_code=403, detail="Not enough permissions")
    query = "SELECT id, email, full_name, company_name, is_active, is_superuser, created_at FROM users"
    user_records = await conn.fetch(query)
    return [dict(record) for record in user_records]