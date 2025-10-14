import base64
import os
import mimetypes

import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from src.config import s3

load_dotenv()


class ProcessResumeInput(BaseModel):
    file_key: str


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


response = process_resume(
    ProcessResumeInput(file_key="user_uploads/c75f6b18-51fc-4803-8a2b-247f1c033511.png")
)


# ---- STEP 1: Download the resume file ----
file_key = "user_uploads/c75f6b18-51fc-4803-8a2b-247f1c033511.png"
image_bytes = process_resume(ProcessResumeInput(file_key=file_key))

# file_path = "resume_image.jpeg"  # or the file_key from S3
# with open(file_path, "rb") as f:
#     image_bytes = f.read()

"""
image_bytes
file_key
"""

# --- Detect MIME type automatically ---
mime_type, _ = mimetypes.guess_type(file_key)

# Fallback in case extension is missing or unknown
if mime_type is None:
    mime_type = "image/png"

# --- Convert to base64 and build data URL ---
base64_img = base64.b64encode(image_bytes).decode("utf-8")
data_url = f"data:{mime_type};base64,{base64_img}"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Encode as base64
base64_img = base64.b64encode(image_bytes).decode("utf-8")

# Build the data URL (important for inline images)
data_url = f"data:image/png;base64,{base64_img}"

# Correct API call
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Please describe the contents of this resume image.",
                },
                {"type": "input_image", "image_url": data_url},
            ],
        }
    ],
)

print(response.output_text)
