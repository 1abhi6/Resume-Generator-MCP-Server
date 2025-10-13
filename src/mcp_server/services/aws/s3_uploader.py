# Upload files to AWS S3 + generate expiring links
import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def upload_to_s3_buffer(file_buffer, bucket_name, object_name):
    """
    Uploads an in-memory file (BytesIO) to S3 and returns a presigned URL.

    Args:
        file_buffer: BytesIO object containing the file to upload.
        bucket_name (str): Name of the S3 bucket.
        object_name (str): S3 object key for the uploaded file.

    Returns:
        str: Presigned URL to access the uploaded file (valid for 1 hour).
    """

    # Create an S3 client using environment credentials
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION"),
    )

    # Upload the file from memory (BytesIO)
    s3.upload_fileobj(file_buffer, bucket_name, object_name)

    # Generate a temporary presigned URL
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=3600,  # 1 hour
    )

    return presigned_url
