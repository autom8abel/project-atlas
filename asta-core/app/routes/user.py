from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.auth.auth_handler import get_password_hash, get_current_user

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

@router.get("/", response_model=List[UserSchema])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Basic protection
):
    """
    Get a list of all users.
    Requires authentication.
    """
    # TODO: Add proper authorization (e.g., only superusers can see all users)
    # For now, we just require any valid authentication
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return [user.to_schema() for user in users]

@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Basic protection
):
    """
    Get a specific user by ID.
    Requires authentication.
    """
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    
    return user.to_schema()
