# Import required modules for loading .docx templates from AWS S3
import os
from io import BytesIO

import boto3
from docxtpl import DocxTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_docx_from_s3(bucket_name: str, key: str) -> DocxTemplate:
    """
    Loads a .docx template directly from S3 into memory.

    Args:
        bucket_name (str): Name of the S3 bucket.
        key (str): S3 object key for the .docx template.

    Returns:
        DocxTemplate: Loaded DocxTemplate object.
    """
    # Initialize S3 client using credentials from environment variables
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION"),
    )

    # Download the .docx file from S3 into a memory buffer
    buffer = BytesIO()
    s3.download_fileobj(bucket_name, key, buffer)
    buffer.seek(0)

    # Load the template from the buffer and return
    return DocxTemplate(buffer)


def get_template_from_s3(template_name: str):
    """
    Helper function to get a .docx template from S3 by template name.

    Args:
        template_name (str): Name of the template (without .docx extension).

    Returns:
        DocxTemplate: Loaded DocxTemplate object.
    """
    # Construct S3 bucket and key from environment variables and template name
    bucket = os.getenv("AWS_S3_BUCKET_NAME")
    key = f"templates/{template_name}.docx"
    return load_docx_from_s3(bucket, key)
