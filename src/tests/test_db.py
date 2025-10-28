import atexit

from src.mcp_server.database import (
    close_database,
    initialize_database,
    resume_repository,
)

# Initialize database on startup
initialize_database()

# Register cleanup on exit
atexit.register(close_database)

try:
    resume_record = resume_repository.create_resume(
        user_id=1,
        template_selected="default",
        pdf_link="",
        doc_link="",
    )
    print(f"Resume record created with ID: {resume_record.id}")
except Exception as e:
    print(f"Error saving resume to database: {e}")
    # Continue even if database save fails
