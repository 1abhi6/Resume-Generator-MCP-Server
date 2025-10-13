"""Database configuration module for Neon PostgreSQL."""

import os
from typing import Optional


class DatabaseConfig:
    """Configuration class for database connection settings."""

    def __init__(self):
        """Initialize database configuration from environment variables."""
        self.database_url: Optional[str] = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

    def get_connection_string(self) -> str:
        """
        Get the database connection string.

        Returns:
            str: PostgreSQL connection string

        Raises:
            ValueError: If DATABASE_URL is not configured
        """
        if not self.database_url:
            raise ValueError("Database URL is not configured")
        return self.database_url


# Global configuration instance
db_config = DatabaseConfig()
