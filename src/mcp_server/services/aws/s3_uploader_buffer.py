# Upload files to AWS S3 + generate expiring links

from src.config import get_aws_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def upload_to_s3_buffer(
    file_buffer, bucket_name, object_name, expiry_in_sec: int = 604800
):
    """
    Uploads an in-memory file (BytesIO) to S3 and returns a presigned URL. For 7 days max

    Args:
        file_buffer: BytesIO object containing the file to upload.
        bucket_name (str): Name of the S3 bucket.
        object_name (str): S3 object key for the uploaded file.

    Returns:
        str: Presigned URL to access the uploaded file.
    """

    # Upload the file from memory (BytesIO)
    s3 = get_aws_client("s3")
    s3.upload_fileobj(file_buffer, bucket_name, object_name)

    # Generate a temporary presigned URL
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expiry_in_sec,
    )

    return presigned_url
