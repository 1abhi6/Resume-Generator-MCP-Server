# App config, env loading, constants

import boto3
import os
from dotenv import load_dotenv

load_dotenv()


# Get AWS client


def get_aws_client(service_name: str = "s3"):
    service_name = service_name.lower()

    client = boto3.client(
        service_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION"),
    )

    return client
