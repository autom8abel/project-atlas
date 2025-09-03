from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base  # Import the Base class we just created

class User(Base):
    """
    ORM model for the 'users' database table.
    Each attribute here maps to a column in the table.
    """

    # The 'id' column is the primary key.
    # `Mapped[int]` defines the Python type, `mapped_column(primary_key=True)` defines the SQL column properties.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # The 'email' column. `unique=True` and `nullable=False` match our SQL constraints.
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    # The 'hashed_password' column. We will never store plain text.
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Optional fields use `Mapped[type | None]`
    full_name: Mapped[str | None] = mapped_column(String(255))
    company_name: Mapped[str | None] = mapped_column(String(255))

    # Boolean flags with default values.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps. We use `server_default` to let PostgreSQL set the value on insert.
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # This is a helpful representation for debugging.
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
