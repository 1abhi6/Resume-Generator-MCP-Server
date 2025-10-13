# Token verification, MCP credentials, etc.
from fastmcp.server.auth import BearerAuthProvider
import os 
from dotenv import load_dotenv

load_dotenv()

auth = BearerAuthProvider(
    jwks_uri=f"{os.getenv('STYTCH_DOMAIN')}/.well-known/jwks.json",
    issuer=os.getenv("STYTCH_DOMAIN"),
    algorithm="RS256",
    audience=os.getenv("STYTCH_PROJECT_ID"),
)
