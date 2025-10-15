import os
from datetime import datetime, timezone
from io import BytesIO

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

from src.mcp_server.agents import LLM
from src.mcp_server.prompts import PromptConfig
from src.mcp_server.schema import (
    ProcessResumeInput,
    TemplateSelectionInput,
)
from src.mcp_server.services import (
    extract_resume_text_from_s3,
    get_openai_vision,
    get_template_from_s3,
    process_resume,
    upload_to_s3_buffer,
)
from src.mcp_server.templates import get_default_context, get_schema
from src.mcp_server.utils import IMAGE_FILE_TYPE, docx_to_pdf


def enhance_resume_for_existing_resume(
    file_key: str, template_name: TemplateSelectionInput
):
    """
    Enhance an existing resume stored in S3 and return signed URLs for DOCX and PDF.

    Params:
    - file_key: S3 key (path) of the existing resume file.
    - template_name: TemplateSelectionInput with template_name attribute.

    Returns:
    - dict with signed URLs for docx and pdf and a human-readable message.
    """
    load_dotenv()

    template_selected = template_name.template_name

    # get the raw file bytes (from S3 or local store)
    file_bytes = process_resume(ProcessResumeInput(file_key=file_key))

    # determine file extension to decide whether to run vision OCR
    file_ext = file_key.lower().split(".")[-1]

    if file_ext in IMAGE_FILE_TYPE:
        # first-pass OCR/description for images
        description = get_openai_vision(image_bytes=file_bytes, file_key=file_key)

    # primary text extraction from the stored object (Textract or equivalent)
    description = extract_resume_text_from_s3(
        bucket_name=os.getenv("AWS_S3_BUCKET_NAME"), file_key=file_key
    )

    # print("TRANSCRIPTION: ", description)

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
    response = llm_obj.get_response(prompt_template=prompt_template)
    enhanced_description = response.content

    # print("\n\n Enhanced Description here:\n", enhanced_description)

    # load template docx and its schema for structured mapping
    doc = get_template_from_s3(template_selected)
    template_schema = get_schema(template_selected)

    # structured LLM maps enhanced text -> pydantic model for the template
    prompt_config = PromptConfig(file_name="central_llm")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    prompt_template = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", enhanced_description),
        ]
    )

    structured_llm_obj = LLM()
    response = structured_llm_obj.get__structured_response(
        resume_pydantic_model=template_schema, prompt_template=prompt_template
    )

    # build rendering context and render the docx template
    context = get_default_context(doc, response)
    # print("CONTEXT BUILT")

    doc.render(context)
    # print("DOCUMENT RENDERED!")

    # save rendered docx to memory and convert to PDF
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    # print("SAVED TO MEMORY")
    pdf_buffer = docx_to_pdf(docx_bytes=buffer.getvalue())

    # create unique S3 keys and upload both docx and pdf (7-day signed URLs)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    docx_object_name = f"resumes/resume_{timestamp}.docx"
    pdf_object_name = f"resumes/resume_{timestamp}.pdf"

    docx_s3_url = upload_to_s3_buffer(
        buffer, os.getenv("AWS_S3_BUCKET_NAME"), docx_object_name, expiry_in_sec=604800
    )

    pdf_s3_url = upload_to_s3_buffer(
        pdf_buffer,
        os.getenv("AWS_S3_BUCKET_NAME"),
        pdf_object_name,
        expiry_in_sec=604800,
    )

    # print("GENERATED RESUME (WORD) UPLOADED TO S3")

    return {
        "docx_resume_url": docx_s3_url,
        "pdf_resume_url": pdf_s3_url,
        "content": "Sucessfully created Resume! You can download it from the links. Link will be expire in 7 days. Use docx to edit if you find anything to otherwise PDF is ready to send! All the best!",
    }


# Example invocation for local testing (keeps the module runnable as a script).
# file_key = "resumes/resume_20251013144653.docx"
# template_name = TemplateSelectionInput(template_name="default")

# response = enhance_resume_for_existing_resume(
#     file_key=file_key, template_name=template_name
# )

# print(response)
