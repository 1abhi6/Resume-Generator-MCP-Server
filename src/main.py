# FastMCP server entry point
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
from src.mcp_server.routes import generate_resume_from_text

load_dotenv()

# Initialize database on startup
initialize_database()

# Register cleanup on exit
atexit.register(close_database)

mcp = FastMCP(name="Resume Generator", auth=auth)


@mcp.tool()
def generate_resume(user_info: str, template_name: str = "default") -> str:
    """Generate a resume based on a description"""
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    response = generate_resume_from_text(
        user_info=user_info, template_name=template_name
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

    return JSONResponse(response)


@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET", "OPTIONS"])
def oauth_metadata(request: StarletteRequest) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/")

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
