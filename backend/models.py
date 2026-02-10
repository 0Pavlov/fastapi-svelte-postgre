# SQLAlchemy ORM to talk to the DB
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


# These classes represent actual tables in PostgreSQL db
class TodoDB(Base):
    """
    Represents the 'todos' table in the database.
    Each instance of this class is a ROW in that table.
    """
    __tablename__ = "todos"

    # 'Mapped[]' SQLAlchemy 2.0 way to define columns
    # with types
    # primary_key=True is the unique ID for the row
    # index=True makes searching by ID faster
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True
    )
    
    # Standard columns 
    # Name is text
    name: Mapped[str] = mapped_column(nullable=False)
    # Desc is text
    description: Mapped[str] = mapped_column(nullable=False)
    # Priority is an integer (1, 2, 3) in the DB
    priority: Mapped[int] = mapped_column(nullable=False)

