from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base properties shared across all schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category: Optional[str] = None  # 'bookkeeping', 'tax', 'invoice'
    is_important: bool = False

# Properties received via API on creation
class TaskCreate(TaskBase):
    pass  # For now, no extra fields needed on creation

# Properties to return via API
class Task(TaskBase):
    id: int
    user_id: int
    status: str  # 'pending', 'in_progress', 'completed'
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows ORM objects to be converted to this schema
