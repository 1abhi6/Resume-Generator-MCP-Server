"""Database package initialization and setup using SQLAlchemy."""

from .config import db_config
from .connection import db_connection
from .models import Base, ResumeRecord
from .repository import resume_repository


def initialize_database() -> None:
    """
    Initialize the database connection and create tables using SQLAlchemy.

    This function should be called once during application startup.

    Raises:
        Exception: If database initialization fails
    """
    try:
        # Initialize SQLAlchemy engine
        db_connection.initialize_engine()

        # Create all tables defined in Base metadata
        Base.metadata.create_all(bind=db_connection.engine)

        print("Database initialized successfully with SQLAlchemy")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise


def close_database() -> None:
    """
    Close database connections and dispose of the engine.

    This function should be called during application shutdown.
    """
    try:
        db_connection.close_engine()
        print("Database connections closed successfully")
    except Exception as e:
        print(f"Error closing database connections: {e}")


__all__ = [
    "db_config",
    "db_connection",
    "Base",
    "ResumeRecord",
    "resume_repository",
    "initialize_database",
    "close_database",
]
