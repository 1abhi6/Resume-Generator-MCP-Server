"""Repository layer for database operations using SQLAlchemy ORM."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, delete, desc

from .connection import db_connection
from .models import ResumeRecord


class ResumeRepository:
    """
    Repository class for resume-related database operations using SQLAlchemy ORM.

    This class provides a clean interface for CRUD operations on the resumes table.
    """

    @staticmethod
    def create_resume(
        user_id: str,
        template_selected: str,
        pdf_link: str,
        doc_link: str,
        date_time: Optional[datetime] = None,
    ) -> ResumeRecord:
        """
        Create a new resume record in the database.

        Args:
            user_id: Unique identifier for the user
            template_selected: Name of the template selected
            pdf_link: URL to the PDF resume
            doc_link: URL to the DOC resume
            date_time: Timestamp (defaults to current time)

        Returns:
            ResumeRecord: The created resume record with ID

        Raises:
            Exception: If database operation fails
        """
        if date_time is None:
            date_time = datetime.now()

        with db_connection.get_session() as session:
            resume = ResumeRecord(
                user_id=user_id,
                template_selected=template_selected,
                pdf_link=pdf_link,
                doc_link=doc_link,
                date_time=date_time,
            )
            session.add(resume)
            session.flush()  # Flush to get the ID before commit
            session.refresh(resume)  # Refresh to get database defaults
            return resume

    @staticmethod
    def get_resume_by_id(resume_id: int) -> Optional[ResumeRecord]:
        """
        Retrieve a resume record by its ID.

        Args:
            resume_id: ID of the resume record

        Returns:
            ResumeRecord if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        with db_connection.get_session() as session:
            stmt = select(ResumeRecord).where(ResumeRecord.id == resume_id)
            result = session.execute(stmt).scalar_one_or_none()
            return result

    @staticmethod
    def get_resumes_by_user(user_id: str, limit: int = 10) -> List[ResumeRecord]:
        """
        Retrieve all resume records for a specific user.

        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of records to return (default: 10)

        Returns:
            List of ResumeRecord objects

        Raises:
            Exception: If database operation fails
        """
        with db_connection.get_session() as session:
            stmt = (
                select(ResumeRecord)
                .where(ResumeRecord.user_id == user_id)
                .order_by(desc(ResumeRecord.date_time))
                .limit(limit)
            )
            result = session.execute(stmt).scalars().all()
            return list(result)

    @staticmethod
    def get_latest_resume_by_user(user_id: str) -> Optional[ResumeRecord]:
        """
        Retrieve the most recent resume record for a user.

        Args:
            user_id: Unique identifier for the user

        Returns:
            ResumeRecord if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        with db_connection.get_session() as session:
            stmt = (
                select(ResumeRecord)
                .where(ResumeRecord.user_id == user_id)
                .order_by(desc(ResumeRecord.date_time))
                .limit(1)
            )
            result = session.execute(stmt).scalar_one_or_none()
            return result

    @staticmethod
    def update_resume_links(
        resume_id: int, pdf_link: Optional[str] = None, doc_link: Optional[str] = None
    ) -> Optional[ResumeRecord]:
        """
        Update the PDF and/or DOC links for a resume record.

        Args:
            resume_id: ID of the resume record
            pdf_link: New PDF link (optional)
            doc_link: New DOC link (optional)

        Returns:
            Updated ResumeRecord if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        if pdf_link is None and doc_link is None:
            raise ValueError("At least one of pdf_link or doc_link must be provided")

        with db_connection.get_session() as session:
            # Get the resume
            resume = session.get(ResumeRecord, resume_id)
            if not resume:
                return None

            # Update fields
            if pdf_link is not None:
                resume.pdf_link = pdf_link
            if doc_link is not None:
                resume.doc_link = doc_link

            session.flush()
            session.refresh(resume)
            return resume

    @staticmethod
    def delete_resume(resume_id: int) -> bool:
        """
        Delete a resume record by its ID.

        Args:
            resume_id: ID of the resume record

        Returns:
            True if deleted successfully, False otherwise

        Raises:
            Exception: If database operation fails
        """
        with db_connection.get_session() as session:
            stmt = delete(ResumeRecord).where(ResumeRecord.id == resume_id)
            result = session.execute(stmt)
            return result.rowcount > 0

    @staticmethod
    def get_all_resumes(limit: int = 100, offset: int = 0) -> List[ResumeRecord]:
        """
        Retrieve all resume records with pagination.

        Args:
            limit: Maximum number of records to return (default: 100)
            offset: Number of records to skip (default: 0)

        Returns:
            List of ResumeRecord objects

        Raises:
            Exception: If database operation fails
        """
        with db_connection.get_session() as session:
            stmt = (
                select(ResumeRecord)
                .order_by(desc(ResumeRecord.date_time))
                .limit(limit)
                .offset(offset)
            )
            result = session.execute(stmt).scalars().all()
            return list(result)


# Global repository instance
resume_repository = ResumeRepository()
