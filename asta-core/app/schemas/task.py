from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

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

# Define allowed values for enums to prevent invalid queries
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskCategory(str, Enum):
    FINANCE = "finance"
    TAX = "tax"
    INVOICE = "invoice"
    REPORTING = "reporting"
    CONSULTATION = "consultation"

# Schema for query parameters
class TaskFilterSort:
    def __init__(
        self,
        status: Optional[TaskStatus] = None,
        category: Optional[TaskCategory] = None,
        is_important: Optional[bool] = None,
        sort_by: Optional[str] = "created_at",  # Default sort
        sort_order: Optional[str] = "desc"      # Default: newest first
    ):
        self.status = status
        self.category = category
        self.is_important = is_important
        self.sort_by = sort_by
        self.sort_order = sort_order
