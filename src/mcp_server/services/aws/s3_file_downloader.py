import os

import requests
from dotenv import load_dotenv

from src.config import s3
from src.mcp_server.schema import ProcessResumeInput

load_dotenv()

def process_resume(input: ProcessResumeInput):
    """Process the uploaded resume and returns byte code."""
    get_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": os.getenv("AWS_S3_BUCKET_NAME"), "Key": input.file_key},
        ExpiresIn=300,
    )
    response = requests.get(get_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")
    return response.content

