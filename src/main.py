# FastMCP server entry point
import os
from datetime import datetime
from io import BytesIO

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.dependencies import AccessToken, get_access_token
from jose import jwt
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse

# from database import NoteRepository
from src.mcp_server.prompts import PromptConfig
from src.mcp_server.templates import default_context
from src.pydantic_schema import ResumeSchema
from src.cloud import upload_to_s3_buffer, get_template_from_s3
from src.utils import make_link, safe_get

load_dotenv()



auth = BearerAuthProvider(
    jwks_uri=f"{os.getenv('STYTCH_DOMAIN')}/.well-known/jwks.json",
    issuer=os.getenv("STYTCH_DOMAIN"),
    algorithm="RS256",
    audience=os.getenv("STYTCH_PROJECT_ID"),
)

mcp = FastMCP(name="Resume Generator", auth=auth)


@mcp.tool()
def generate_resume(user_info: str) -> str:
    """Generate a resume based on a description"""
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    doc = get_template_from_s3("default")

    text = user_info

    prompt_config = PromptConfig(file_name="central_llm")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    prompt_template = ChatPromptTemplate(
        [
            ("system",system_prompt),
            ("human", text),
        ]
    )

    model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    structured_model = model.with_structured_output(ResumeSchema)
    chain = prompt_template | structured_model

    response = chain.invoke({})

    # default_context Dict Here
    
    print(default_context)

    doc.render(default_context)

    doc.render(default_context)

    # Save to memory instead of disk
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # Unique object name for S3
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    object_name = f"resumes/resume_{timestamp}.docx"

    # Upload in-memory bytes to S3
    s3_url = upload_to_s3_buffer(buffer, os.getenv("AWS_S3_BUCKET"), object_name)

    print("✅ Resume uploaded to S3:", s3_url)

    return JSONResponse(
        {
            "resume_url": s3_url,
            "content": "Sucessfully created Resume! You can download it from the link."
        }
    )



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

