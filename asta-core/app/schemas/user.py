from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Base properties shared across all schemas
class UserBase(BaseModel):
    email: EmailStr  # This validates that the input is a proper email format
    full_name: Optional[str] = None
    company_name: Optional[str] = None

# Properties received via API on creation
class UserCreate(UserBase):
    password: str  # We will receive a plain password, then hash it before saving

# Properties to return via API (we never return the password!)
class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    # This tells Pydantic to work with ORM objects, not just dicts
    class Config:
        from_attributes = True  # Previously 'orm_mode = True' in Pydantic v1

# Schema for the login request body
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for the successful login response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for the token data embedded within the JWT
class TokenData(BaseModel):
    id: str | None = None