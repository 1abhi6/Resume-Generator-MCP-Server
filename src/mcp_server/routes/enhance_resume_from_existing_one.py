import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

from src.mcp_server.agents import LLM
from src.mcp_server.prompts import PromptConfig
from src.mcp_server.schema import ProcessResumeInput
from src.mcp_server.services import (
    extract_resume_text_from_s3,
    get_openai_vision,
    process_resume,
)
from src.mcp_server.utils import IMAGE_FILE_TYPE
from src.mcp_server.routes.common_logic import get_common_logic


def enhance_resume_for_existing_resume(file_key: str, template_selected: str) -> dict:
    """
    Enhance an existing resume stored in S3 and return signed URLs for DOCX and PDF.

    Params:
    - file_key: S3 key (path) of the existing resume file.
    - template_selected: Template selected by the user.

    Returns:
    - dict with signed URLs for docx and pdf and a human-readable message.
    """
    load_dotenv()

    # get the raw file bytes (from S3 or local store)
    file_bytes = process_resume(ProcessResumeInput(file_key=file_key))

    # determine file extension to decide whether to run vision OCR
    file_ext = file_key.lower().split(".")[-1]

    if file_ext in IMAGE_FILE_TYPE:
        # first-pass OCR/description for images
        description = get_openai_vision(image_bytes=file_bytes, file_key=file_key)

    # primary text extraction from the stored object (Textract or equivalent)
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    description = extract_resume_text_from_s3(
        bucket_name=bucket_name, file_key=file_key
    )

    # use LLM to clean/enhance the extracted transcription
    prompt_config = PromptConfig(file_name="ocr")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    prompt_template = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", description),
        ]
    )

    llm_obj = LLM()
    enhanced_persona = llm_obj.get_response(prompt_template=prompt_template)

    response = get_common_logic(
        enhanced_description=enhanced_persona,
        template_selected=template_selected,
        bucket_name=bucket_name,
    )

    return response


# file_key = "resumes/resume_20251013144653.docx"
# template_name = "default"

# response = enhance_resume_for_existing_resume(
#     file_key=file_key, template_selected=template_name
# )

# print(response)
