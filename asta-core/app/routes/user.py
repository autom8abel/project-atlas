from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.auth.auth_handler import get_password_hash

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user.
    - Checks if email already exists.
    - Hashes the password before storing.
    - Saves the new user to the database.
    - Returns the created user (without password).
    """
    # 1. Check if user with email already exists
    existing_user_query = select(User).where(User.email == user_data.email)
    result = await db.execute(existing_user_query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    # 2. Hash the password
    hashed_password = get_password_hash(user_data.password)

    # 3. Create new user object
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        company_name=user_data.company_name,
    )

    # 4. Add to database and commit
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Refresh to get the database-generated values like ID

    # 5. Return the created user (matches UserSchema which excludes password)
    return new_user
