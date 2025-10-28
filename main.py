import atexit
import os

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.dependencies import AccessToken, get_access_token
from jose import jwt
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse

from src.mcp_server.auth import auth
from src.mcp_server.database import (
    close_database,
    initialize_database,
    resume_repository,
)
from src.mcp_server.routes import (
    enhance_resume_for_existing_resume,
    generate_resume_from_text,
    job_match,
    linkedin,
)
from src.mcp_server.schema import TemplateSelectionInput
from src.mcp_server.services import (
    get_file_info_from_s3,
    upload_resume_from_filesystem,
)

load_dotenv()

# Initialize database on startup
initialize_database()

# Register cleanup on exit
atexit.register(close_database)

mcp = FastMCP(name="Resume Generator", auth=auth)


# Health Check Tool
@mcp.tool(
    name="check_server_health",
    description=(
        "Verify that the Resume Generator MCP Server is running and accessible. "
        "Use this tool to check the health status of the server and confirm that "
        "the user's authentication token is valid. "
        "It returns the current user's ID and a simple health status ('ok' if operational)."
    ),
)
def check_server_health_status() -> dict:
    """
    Performs a health check on the Resume Generator MCP Server.

    **Purpose:**
    - Ensures that the server is up and responding to requests.
    - Validates that the user's authentication token is active.

    **Output:**
    - Returns a JSONResponse containing:
        {
            "user_id": "<authenticated user ID>",
            "status": "ok" | "unauthorized"
        }

    **Example:**
    ```json
    {
        "user_id": "user-12345",
        "status": "ok"
    }
    ```
    """
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token).get("sub")

    status = "ok" if user_id else "unauthorized"

    return {"user_id": user_id, "status": status}


# Generate Resume from raw input Tool
@mcp.tool(
    name="generate_resume_from_text",
    description=(
        "Generate a complete, ATS-friendly resume using raw text input. "
        "Use this tool when the user provides a plain text description of their experience, "
        "skills, or background (not an existing file or LinkedIn URL). "
        "The user must also specify a resume template name (e.g., 'modern', 'classic'). "
        "This tool returns temporary download links (PDF and DOCX) for the generated resume."
    ),
)
def generate_resume_from_text_tool(
    user_info: str, template_name: TemplateSelectionInput
) -> dict:
    """
    Generates a resume using free-form user-provided text and a selected template.

    **Use this tool when:**
    - The user provides their professional background, skills, and experience in plain text.
    - The user specifies which predefined resume template to use.

    **Inputs:**
    - `user_info` (str): The user's background, experience, and skills in text format.
    - `template_name` (TemplateSelectionInput): The name of the predefined template to render.

    **Output:**
    - Returns a JSONResponse containing:
        {
            "docx_resume_url": "<S3 link to Word resume>",
            "pdf_resume_url": "<S3 link to PDF resume>",
            "content:: "A general message"
        }
    """
    # access_token: AccessToken = get_access_token()
    # user_id = jwt.get_unverified_claims(access_token.token)["sub"]
    initialize_database()

    # Register cleanup on exit
    atexit.register(close_database)
    user_id = 1

    template: str = template_name.template_name

    response = generate_resume_from_text(user_info=user_info, template_name=template)

    docx_link = response.get("docx_resume_url")
    pdf_link = response.get("pdf_resume_url")

    # Save resume data to database
    try:
        resume_record = resume_repository.create_resume(
            user_id=user_id,
            template_selected=template_name,
            pdf_link=pdf_link or "",
            doc_link=docx_link or "",
        )
        print(f"Resume record created with ID: {resume_record.id}")
    except Exception as e:
        print(f"Error saving resume to database: {e}")
        # Continue even if database save fails

    return response


# Upload Reume From file tool
@mcp.tool()
async def upload_resume_file(file_path: str) -> dict:
    """
    Upload a resume file directly from the local filesystem to S3.
    Use this tool when the user provides a resume file path.

    Args:
        file_path: Absolute path to the resume file (PDF, DOCX, PNG, JPG, JPEG)

    Returns:
        dict with file_key that can be used with resume-enhancer or generate-resume-from-jd-and-existing
    """
    return upload_resume_from_filesystem(file_path)


# Check Uploaded file exists in S3
@mcp.tool()
async def check_uploaded_file(file_key: str) -> dict:
    """
    Check if a file exists in S3 and get its metadata.

    Args:
        file_key: The S3 key of the uploaded file

    Returns:
        dict with file information
    """
    return get_file_info_from_s3(file_key)


# Upload file and select resume (Resume Enhancer)
@mcp.tool(
    name="resume-enhancer",
    description="Enhance an uploaded resume using a selected template; returns DOCX and PDF download URLs and saves a resume record (non-blocking).",
)
def enhance_resume_from_existing(file_key: str, template_name: TemplateSelectionInput):
    """
    Enhance an existing resume with a chosen template and return download links.

    Parameters
    - file_key: AWS File Key
    - template_name: Name of the template

    Returns: JSONResponse containing:
                {
                    "docx_resume_url": "<S3 link to Word resume>",
                    "pdf_resume_url": "<S3 link to PDF resume>",
                    "content": "A general message"
                }
    """
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    template_selected = template_name.template_name

    response = enhance_resume_for_existing_resume(
        file_key=file_key, template_selected=template_selected
    )

    docx_link = response.get("docx_resume_url")
    pdf_link = response.get("pdf_resume_url")

    # Save resume data to database
    try:
        resume_record = resume_repository.create_resume(
            user_id=user_id,
            template_selected=template_name,
            pdf_link=pdf_link or "",
            doc_link=docx_link or "",
        )
        print(f"Resume record created with ID: {resume_record.id}")
    except Exception as e:
        print(f"Error saving resume to database: {e}")
        # Continue even if database save fails

    return response


# Generate Resume from Job Description and Existing Resume
@mcp.tool(
    title="generate-resume-from-job-description-and-existing-resume",
    description="Generates a tailored resume by combining an existing resume with a provided job description using the selected template.",
)
def generate_resume_from_jd_and_existing(
    file_key: str,
    template_name: TemplateSelectionInput,
    job_descrption: str,
):
    """
    Generate a new, customized resume by aligning the user’s existing resume
    with a provided job description and rendering it using a chosen template.

    Args:
        file_key: The file key from S3
        template_name (TemplateSelectionInput): The selected resume template name.
        job_descrption (str): The job description text used to tailor the resume.

    Returns:
        JSONResponse: A JSON response containing presigned S3 links for the generated
                      DOCX and PDF resumes along with related metadata.
    """

    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    template_selected = template_name.template_name

    response = job_match(
        file_key=file_key,
        template_selected=template_selected,
        job_description=job_descrption,
    )

    docx_link = response.get("docx_resume_url")
    pdf_link = response.get("pdf_resume_url")

    # Save resume data to database
    try:
        resume_record = resume_repository.create_resume(
            user_id=user_id,
            template_selected=template_name,
            pdf_link=pdf_link or "",
            doc_link=docx_link or "",
        )
        print(f"Resume record created with ID: {resume_record.id}")
    except Exception as e:
        print(f"Error saving resume to database: {e}")
        # Continue even if database save fails

    return response


# Get resume from Linkedin URL
@mcp.tool(
    title="generate-resume-from-linkedin-profile",
    description=(
        "Generates a professional, ready-to-send resume directly from a user's LinkedIn profile. "
        "The tool scrapes structured data from the provided LinkedIn URL, processes it through AI-based "
        "resume extraction and formatting pipelines, and renders a resume using the selected template. "
        "Outputs include both a downloadable Word (.docx) and PDF version of the generated resume, "
        "each stored temporarily on AWS S3 with an expiring link."
    ),
)
def generate_resume_from_linkedin_profile(
    linkedin_url: str,
    template_name: TemplateSelectionInput,
):
    """
    Generate a professional resume directly from a LinkedIn profile URL using a predefined template.

    This MCP tool automates the process of transforming a user’s LinkedIn data into an ATS-friendly,
    template-based resume. It extracts and structures the information from the LinkedIn profile,
    formats it using the selected Jinja2/Docx template, and uploads the resulting files to AWS S3.

    Parameters
    ----------
    linkedin_url: A validated LinkedIn profile URL provided by the user.
    template_name: TemplateSelectionInput
        The name of the predefined resume template selected by the user.

    Returns
    -------
    JSONResponse
        A JSON response containing:
            - `docx_resume_url`: AWS S3 link to the generated Word resume.
            - `pdf_resume_url`: AWS S3 link to the generated PDF resume.
        Both links are temporary and automatically expire within 7 hours.
    """

    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    template_selected = template_name.template_name

    # Get response from LinkedIn
    response = linkedin(linkedin_url=linkedin_url, template_selected=template_selected)

    docx_link = response.get("docx_resume_url")
    pdf_link = response.get("pdf_resume_url")

    # Save resume data to database
    try:
        resume_record = resume_repository.create_resume(
            user_id=user_id,
            template_selected=template_name,
            pdf_link=pdf_link or "",
            doc_link=docx_link or "",
        )
        print(f"Resume record created with ID: {resume_record.id}")
    except Exception as e:
        print(f"Error saving resume to database: {e}")
        # Continue even if database save fails

    return response


# Auth Custom Route
@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET", "OPTIONS"])
def oauth_metadata(request: StarletteRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")

    print(base_url)

    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"],
        }
    )


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
    )
