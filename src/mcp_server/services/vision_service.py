# Image OCR/desctiption using OpenAI Vision

import base64
import mimetypes
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.mcp_server.schema import ProcessResumeInput

load_dotenv()


def get_openai_vision(image_bytes, file_key: ProcessResumeInput) -> str:
    # --- Detect MIME type automatically ---
    mime_type, _ = mimetypes.guess_type(file_key.file_key)

    # Fallback in case extension is missing or unknown
    if mime_type is None:
        mime_type = "image/png"

    # Convert to base64 and build data URL
    base64_img = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{base64_img}"

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Encode as base64
    base64_img = base64.b64encode(image_bytes).decode("utf-8")

    # Build the data URL
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

    return response.output_text
