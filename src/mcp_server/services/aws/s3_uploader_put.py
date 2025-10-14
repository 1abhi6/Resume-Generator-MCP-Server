import os
import uuid

from dotenv import load_dotenv

from src.config import s3
from src.mcp_server.schema import UploadURLInput, UploadURLResponse
from src.mcp_server.utils import VALID_FILE_TYPES

load_dotenv()


def get_upload_url(input: UploadURLInput) -> UploadURLResponse:
    """
    Generate a pre-signed S3 upload URL for a user file.

    Args:
        input (UploadURLInput): Input containing file type.

    Returns:
        UploadURLResponse: Contains the upload URL and the generated S3 file key.
    """
    file_type = input.file_type
    # Use 'jpg' extension for 'jpeg' file type, otherwise use the file_type as extension
    key_ext = "jpg" if file_type == "jpeg" else file_type

    # Generate a unique S3 key for the uploaded file
    key = f"user_uploads/{uuid.uuid4()}.{key_ext}"

    # Get the correct content type for the file
    content_type = VALID_FILE_TYPES[file_type]

    # Generate a pre-signed URL for uploading the file to S3
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
    return UploadURLResponse(upload_url=upload_url, file_key=key)
