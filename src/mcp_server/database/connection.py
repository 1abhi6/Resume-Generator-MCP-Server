"""Database connection management module using SQLAlchemy."""

from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import QueuePool

from .config import db_config


class DatabaseConnection:
    """
    Database connection manager using SQLAlchemy.

    This class manages the SQLAlchemy engine and session factory,
    providing thread-safe access to database sessions with connection pooling.
    """

    def __init__(
        self,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 3600,
    ):
        """
        Initialize the database connection manager.

        Args:
            pool_size: Number of connections to maintain in the pool
            max_overflow: Maximum number of connections to create beyond pool_size
            pool_timeout: Seconds to wait before giving up on getting a connection
            pool_recycle: Seconds after which to recycle connections (prevents stale connections)
        """
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._scoped_session_factory: Optional[scoped_session] = None
        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._pool_timeout = pool_timeout
        self._pool_recycle = pool_recycle

    def initialize_engine(self) -> None:
        """
        Initialize the SQLAlchemy engine and session factory.

        Raises:
            Exception: If engine initialization fails
        """
        try:
            # Create engine with connection pooling
            self._engine = create_engine(
                db_config.get_connection_string(),
                poolclass=QueuePool,
                pool_size=self._pool_size,
                max_overflow=self._max_overflow,
                pool_timeout=self._pool_timeout,
                pool_recycle=self._pool_recycle,
                pool_pre_ping=True,  # Verify connections before using them
                echo=False,  # Set to True for SQL query logging
            )

            # Create session factory
            self._session_factory = sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )

            # Create scoped session factory for thread-safe sessions
            self._scoped_session_factory = scoped_session(self._session_factory)

            print("SQLAlchemy engine and session factory initialized successfully")
        except Exception as e:
            print(f"Error initializing SQLAlchemy engine: {e}")
            raise

    def close_engine(self) -> None:
        """Close the SQLAlchemy engine and dispose of the connection pool."""
        if self._scoped_session_factory:
            self._scoped_session_factory.remove()

        if self._engine:
            self._engine.dispose()
            print("SQLAlchemy engine closed and connections disposed")

    @contextmanager
    def get_session(self) -> Session:
        """
        Get a database session using context manager.

        Yields:
            Session: SQLAlchemy database session

        Raises:
            Exception: If session factory is not initialized or session fails

        Example:
            with db_connection.get_session() as session:
                user = session.query(User).first()
        """
        if not self._session_factory:
            raise Exception("Session factory is not initialized. Call initialize_engine() first.")

        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def get_scoped_session(self) -> scoped_session:
        """
        Get a scoped session for thread-safe operations.

        Returns:
            scoped_session: Thread-local session

        Raises:
            Exception: If session factory is not initialized
        """
        if not self._scoped_session_factory:
            raise Exception("Scoped session factory is not initialized. Call initialize_engine() first.")
        return self._scoped_session_factory

    @property
    def engine(self) -> Engine:
        """
        Get the SQLAlchemy engine.

        Returns:
            Engine: SQLAlchemy engine

        Raises:
            Exception: If engine is not initialized
        """
        if not self._engine:
            raise Exception("Engine is not initialized. Call initialize_engine() first.")
        return self._engine


# Global database connection instance
db_connection = DatabaseConnection()
