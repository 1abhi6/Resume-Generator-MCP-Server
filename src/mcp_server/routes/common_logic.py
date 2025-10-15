# load template docx and its schema for structured mapping
import os
from datetime import datetime, timezone
from io import BytesIO

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

from src.mcp_server.agents import LLM
from src.mcp_server.prompts import PromptConfig
from src.mcp_server.services import (
    get_template_from_s3,
    upload_to_s3_buffer,
)
from src.mcp_server.templates import get_default_context, get_schema
from src.mcp_server.utils import docx_to_pdf

load_dotenv()


def get_common_logic(
    enhanced_persona: str,
    template_selected: str,
    bucket_name: str = os.getenv("AWS_S3_BUCKET_NAME"),
):
    doc = get_template_from_s3(template_selected)
    template_schema = get_schema(template_selected)

    # structured LLM maps enhanced text -> pydantic model for the template
    prompt_config = PromptConfig(file_name="central_llm")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    prompt_template = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", enhanced_persona),
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
        file_buffer=buffer,
        bucket_name=bucket_name,
        object_name=docx_object_name,
        expiry_in_sec=604800,
    )

    pdf_s3_url = upload_to_s3_buffer(
        file_buffer=pdf_buffer,
        bucket_name=bucket_name,
        object_name=pdf_object_name,
        expiry_in_sec=604800,
    )

    # print("GENERATED RESUME (WORD) UPLOADED TO S3")

    return {
        "docx_resume_url": docx_s3_url,
        "pdf_resume_url": pdf_s3_url,
        "content": "Sucessfully created Resume! You can download it from the links. Link will be expire in 7 days. Use docx to edit if you find anything to otherwise PDF is ready to send! All the best!",
    }
