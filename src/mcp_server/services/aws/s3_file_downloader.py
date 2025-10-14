"""
Service for downloading files from AWS S3 using a presigned URL.

This module handles authentication, presigned URL generation, and file retrieval.
Used to fetch resume files for further processing in the application.
"""

import os

import requests
from dotenv import load_dotenv

from src.config import get_aws_client
from src.mcp_server.schema import ProcessResumeInput

load_dotenv()


def process_resume(input: ProcessResumeInput):
    """Process the uploaded resume and returns byte code."""
    s3 = get_aws_client("s3")

    get_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": os.getenv("AWS_S3_BUCKET_NAME"), "Key": input.file_key},
        ExpiresIn=300,
    )
    response = requests.get(get_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")
    return response.content
