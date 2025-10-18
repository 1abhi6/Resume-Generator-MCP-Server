import os
import uuid
from pathlib import Path

from dotenv import load_dotenv

from src.config import get_aws_client
from src.mcp_server.schema import UploadURLInput, UploadURLResponse
from src.mcp_server.utils import VALID_FILE_TYPES

load_dotenv()


def get_upload_url(filename: str, content_type: str) -> dict:
    """
    Generate a pre-signed S3 upload URL for a user file.

    Args:
        filename (str): Name of the file
        content_type (str): MIME type of the file

    Returns:
        dict: Contains the upload URL and the generated S3 file key.
    """
    # Generate unique file key
    file_extension = filename.split(".")[-1] if "." in filename else ""
    key = f"user_uploads/{uuid.uuid4()}.{file_extension}"

    # Generate a pre-signed URL for uploading the file to S3
    s3 = get_aws_client("s3")
    upload_url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": os.getenv("AWS_S3_BUCKET_NAME"),
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=900,
    )

    # Return the upload URL and file key in the response
    return {
        "upload_url": upload_url,
        "file_key": key,
        "instructions": "Upload your file to this URL, then call resume-enhancer or generate-resume-from-job-description-and-existing-resume with the file_key",
    }


def upload_resume_from_filesystem(file_path: str) -> dict:
    """
    Upload a resume file directly from the local filesystem to S3.
    This is designed for MCP clients that can read files but cannot make HTTP PUT requests.

    Args:
        file_path (str): Absolute path to the resume file on the local filesystem

    Returns:
        dict: Contains the S3 file key and status message

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file type is not supported
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Get file extension and validate
    file_extension = Path(file_path).suffix.lower().lstrip(".")

    # Map extensions to content types
    content_type_map = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "doc": "application/msword",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
    }

    if file_extension not in content_type_map:
        raise ValueError(
            f"Unsupported file type: .{file_extension}. "
            f"Supported types: {', '.join(content_type_map.keys())}"
        )

    content_type = content_type_map[file_extension]

    # Generate unique S3 key
    key = f"user_uploads/{uuid.uuid4()}.{file_extension}"

    # Read file content
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Upload to S3
    s3 = get_aws_client("s3")
    s3.put_object(
        Bucket=os.getenv("AWS_S3_BUCKET_NAME"),
        Key=key,
        Body=file_content,
        ContentType=content_type,
    )

    # Return the file key
    return {
        "file_key": key,
        "status": "success",
        "message": f"File uploaded successfully from {file_path}",
        "file_type": file_extension,
        "s3_location": f"s3://{os.getenv('AWS_S3_BUCKET_NAME')}/{key}",
    }


def get_file_info_from_s3(file_key: str) -> dict:
    """
    Get metadata about an uploaded file from S3.

    Args:
        file_key (str): The S3 key of the file

    Returns:
        dict: File metadata including size, content type, etc.
    """
    s3 = get_aws_client("s3")

    try:
        response = s3.head_object(Bucket=os.getenv("AWS_S3_BUCKET_NAME"), Key=file_key)

        return {
            "file_key": file_key,
            "exists": True,
            "size_bytes": response.get("ContentLength"),
            "content_type": response.get("ContentType"),
            "last_modified": response.get("LastModified").isoformat()
            if response.get("LastModified")
            else None,
        }
    except Exception as e:
        return {"file_key": file_key, "exists": False, "error": str(e)}
