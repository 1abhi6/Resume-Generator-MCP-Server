"""Simple test script for database operations."""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

from src.mcp_server.database import initialize_database, close_database, resume_repository


def test_database_operations():
    """Test basic database operations."""
    print("=" * 60)
    print("Testing SQLAlchemy Database Setup")
    print("=" * 60)

    try:
        # Initialize database
        print("\n1. Initializing database...")
        initialize_database()
        print("✓ Database initialized successfully")

        # Test creating a resume
        print("\n2. Creating a test resume record...")
        test_resume = resume_repository.create_resume(
            user_id="test_user_123",
            template_selected="modern",
            pdf_link="https://example.com/resume.pdf",
            doc_link="https://example.com/resume.docx",
        )
        print(f"✓ Resume created with ID: {test_resume.id}")
        print(f"   User ID: {test_resume.user_id}")
        print(f"   Template: {test_resume.template_selected}")
        print(f"   Created at: {test_resume.created_at}")

        # Test retrieving by ID
        print(f"\n3. Retrieving resume by ID {test_resume.id}...")
        retrieved = resume_repository.get_resume_by_id(test_resume.id)
        if retrieved:
            print(f"✓ Retrieved resume: {retrieved.user_id} - {retrieved.template_selected}")
        else:
            print("✗ Failed to retrieve resume")

        # Test retrieving by user
        print(f"\n4. Retrieving resumes for user '{test_resume.user_id}'...")
        user_resumes = resume_repository.get_resumes_by_user(test_resume.user_id)
        print(f"✓ Found {len(user_resumes)} resume(s) for user")

        # Test updating links
        print(f"\n5. Updating resume links...")
        updated = resume_repository.update_resume_links(
            test_resume.id,
            pdf_link="https://example.com/updated.pdf",
            doc_link="https://example.com/updated.docx",
        )
        if updated:
            print(f"✓ Updated resume links")
            print(f"   New PDF: {updated.pdf_link}")
            print(f"   New DOC: {updated.doc_link}")
        else:
            print("✗ Failed to update resume")

        # Test getting latest resume
        print(f"\n6. Getting latest resume for user...")
        latest = resume_repository.get_latest_resume_by_user(test_resume.user_id)
        if latest:
            print(f"✓ Latest resume ID: {latest.id}")
        else:
            print("✗ Failed to get latest resume")

        # Test deleting
        print(f"\n7. Deleting test resume...")
        deleted = resume_repository.delete_resume(test_resume.id)
        if deleted:
            print("✓ Resume deleted successfully")
        else:
            print("✗ Failed to delete resume")

        # Verify deletion
        print(f"\n8. Verifying deletion...")
        verify = resume_repository.get_resume_by_id(test_resume.id)
        if verify is None:
            print("✓ Resume successfully deleted (not found)")
        else:
            print("✗ Resume still exists after deletion")

        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        print("\nClosing database connection...")
        close_database()
        print("✓ Database connection closed")


if __name__ == "__main__":
    test_database_operations()
