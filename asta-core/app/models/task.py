from sqlalchemy import ForeignKey, String, Text, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

# Import User only for type checking to avoid circular imports
if TYPE_CHECKING:
    from app.models.user import User

class Task(Base):
    """
    ORM model for the 'tasks' database table.
    Represents a task belonging to a user.
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # ForeignKey to link to the users table. This is the critical line.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    due_date: Mapped[datetime | None] = mapped_column(DateTime)
    
    # Finance-focused categories for your niche
    category: Mapped[str | None] = mapped_column(String(100))  # 'bookkeeping', 'tax', 'invoice'
    
    status: Mapped[str] = mapped_column(String(50), default='pending')  # 'pending', 'in_progress', 'completed'
    is_important: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Define the relationship to the User model for convenient data access
    user: Mapped["User"] = relationship("User", back_populates="tasks")

    def to_schema(self):
        """Convert ORM model to Pydantic schema compatible dict."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "category": self.category,
            "status": self.status,
            "is_important": self.is_important,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title})>"
