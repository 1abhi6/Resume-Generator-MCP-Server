import os
import uuid

from src.config import s3
from dotenv import load_dotenv
from src.mcp_server.utils import VALID_FILE_TYPES
from src.mcp_server.schema import UploadURLInput, UploadURLResponse

load_dotenv()


def get_upload_url(input: UploadURLInput) -> UploadURLResponse:
    """Generate a pre-signed S3 upload URL for a user file."""
    file_type = input.file_type
    key_ext = "jpg" if file_type == "jpeg" else file_type
    key = f"user_uploads/{uuid.uuid4()}.{key_ext}"
    content_type = VALID_FILE_TYPES[file_type]

    upload_url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": os.getenv("AWS_S3_BUCKET_NAME"),
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=900,
    )

    return UploadURLResponse(upload_url=upload_url, file_key=key)


# You must create the input model:
response = get_upload_url(UploadURLInput(file_type="pdf"))

print(response)
