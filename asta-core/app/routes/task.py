from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, Task as TaskSchema, TaskFilterSort, TaskStatus, TaskCategory
from typing import Optional
from app.auth.auth_handler import get_current_user

def validate_sort_params(sort_by: str, sort_order: str) -> None:
    """Validate sort parameters and raise HTTPException if invalid."""
    valid_sort_fields = {"created_at", "updated_at", "due_date", "title"}
    valid_sort_orders = {"asc", "desc"}
    
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort field '{sort_by}'. Must be one of: {valid_sort_fields}"
        )
    
    if sort_order not in valid_sort_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort order '{sort_order}'. Must be 'asc' or 'desc'"
        )

router = APIRouter()

# All routes in this file are protected by authentication
@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task for the authenticated user."""
    new_task = Task(
        **task_data.dict(),
        user_id=current_user.id,  # Automatically assign task to the current user
        status='pending'  # Default status
    )
    
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    
    return new_task

@router.get("/", response_model=List[TaskSchema])
async def get_user_tasks(
    status: Optional[TaskStatus] = None,
    category: Optional[TaskCategory] = None,
    is_important: Optional[bool] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks for the authenticated user with filtering and sorting.
    
    Query Parameters:
    - status: Filter by status (pending, in_progress, completed)
    - category: Filter by category (finance, tax, invoice, reporting, consultation)
    - is_important: Filter by importance (true/false)
    - sort_by: Field to sort by (created_at, updated_at, due_date, title)
    - sort_order: Sort order (asc, desc)
    """
    # Start with base query - only tasks for current user
    query = select(Task).where(Task.user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.where(Task.status == status)
    if category:
        query = query.where(Task.category == category)
    if is_important is not None:  # Could be False, which is valid
        query = query.where(Task.is_important == is_important)
    

    # Validate and apply sorting
    validate_sort_params(sort_by, sort_order)  # Use the new helper function
    
    if sort_order.lower() == "asc":
        query = query.order_by(getattr(Task, sort_by).asc())
    else:
        query = query.order_by(getattr(Task, sort_by).desc())
    
    # Execute query
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return tasks

@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific task by ID. User can only access their own tasks."""
    query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    
    return task

@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a specific task. User can only update their own tasks."""
    query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    
    # Update the task attributes
    for field, value in task_data.dict().items():
        setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific task. User can only delete their own tasks."""
    query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    
    await db.delete(task)
    await db.commit()
    
    return None  # 204 No Content response
