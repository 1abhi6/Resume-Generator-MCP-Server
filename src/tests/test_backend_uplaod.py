# import requests

# upload_url='https://chatbot-attachments-abhi.s3.amazonaws.com/user_uploads/c75f6b18-51fc-4803-8a2b-247f1c033511.png?AWSAccessKeyId=AKIATQZCSDGOZ6SNOSVZ&Signature=aoXatv7vZYOL93lLPcxfBA%2F6ZyA%3D&content-type=image%2Fpng&Expires=1760435028'

# file_key='user_uploads/c75f6b18-51fc-4803-8a2b-247f1c033511.png'

# with open("highlevel-architecture.png", "rb") as f:
#     file_bytes = f.read()
#     headers = {"Content-Type": "image/png"}
#     response = requests.put(upload_url, data=file_bytes, headers=headers)
#     print(response)
#     print("Status:", response.status_code)


import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read your S3-downloaded bytes or local image
with open("highlevel-architecture.png", "rb") as f:
    image_bytes = f.read()

# Encode as base64
base64_img = base64.b64encode(image_bytes).decode("utf-8")

# Build the data URL (important for inline images)
data_url = f"data:image/png;base64,{base64_img}"

# Correct API call
response = client.responses.create(
    model="gpt-4o-mini",  # or "gpt-4.1"
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Please describe the contents of this resume image."},
                {"type": "input_image", "image_url": data_url},
            ],
        }
    ],
)

print(response.output_text)
