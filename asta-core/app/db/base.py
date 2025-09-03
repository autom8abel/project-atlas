from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs

# Create a base class for all ORM models to inherit from.
# Using `AsyncAttrs` provides support for lazy-loaded attributes in async mode.
class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    This provides a common foundation and allows us to avoid repeating code.
    """

    # This generates a default __tablename__ from the class name.
    # e.g., a class named 'User' will have a table name 'users'.
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
