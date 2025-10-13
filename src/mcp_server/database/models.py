"""Database models and schema definitions using SQLAlchemy."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class ResumeRecord(Base):
    """
    SQLAlchemy model representing a resume record in the database.

    Attributes:
        id: Auto-generated primary key
        user_id: Unique identifier for the user (from Stytch)
        template_selected: Name of the template selected by the user
        pdf_link: 7-day expiry link for the generated PDF resume
        doc_link: 7-day expiry link for the generated DOC resume
        date_time: Timestamp when the record was created
        created_at: Timestamp when the record was first created
        updated_at: Timestamp when the record was last updated
    """

    __tablename__ = "resumes"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Required fields
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    template_selected: Mapped[str] = mapped_column(String(100), nullable=False)
    pdf_link: Mapped[str] = mapped_column(Text, nullable=False)
    doc_link: Mapped[str] = mapped_column(Text, nullable=False)

    # Timestamps
    date_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_user_id_date", "user_id", "date_time"),
        Index("idx_date_time_desc", "date_time"),
    )

    def to_dict(self) -> dict:
        """
        Convert the ResumeRecord to a dictionary.

        Returns:
            dict: Dictionary representation of the resume record
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "template_selected": self.template_selected,
            "pdf_link": self.pdf_link,
            "doc_link": self.doc_link,
            "date_time": self.date_time.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation of the ResumeRecord."""
        return f"<ResumeRecord(id={self.id}, user_id={self.user_id}, template={self.template_selected})>"
