# Tool for job desc + resume
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


def job_match(file_key: str, template_selected: str, job_description: str) -> dict:
    """
    Generates a new resume based on Job description stored in S3 and return signed URLs for DOCX and PDF.

    Params:
    - file_key: S3 key (path) of the existing resume file.
    - template_selected: Template selected by the user.
    - job_description: Job description

    Returns:
    - dict with signed URLs for docx and pdf and a human-readable message.
    """
    load_dotenv()

    # get the raw file bytes (from S3 or local store)
    file_bytes = process_resume(ProcessResumeInput(file_key=file_key))

    # determine file extension to decide whether to run vision OCR
    file_ext = file_key.lower().split(".")[-1]

    if file_ext in IMAGE_FILE_TYPE:
        description = get_openai_vision(image_bytes=file_bytes, file_key=file_key)

    # primary text extraction from the stored object (Textract)
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    description = extract_resume_text_from_s3(
        bucket_name=bucket_name, file_key=file_key
    )

    print("GOT DESCRIPTION")
    # Enhance Transcription/OCR
    prompt_config = PromptConfig(file_name="ocr")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    print("System Prompt: ", system_prompt)

    prompt_template = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", description),
        ]
    )

    print("Prompt Template: ", prompt_template)

    llm_obj = LLM()
    enhanced_persona = llm_obj.get_response(prompt_template=prompt_template)
    print(":::::::::::::::::ENHANCED PERSONA::::::::::::::::::::::\n", enhanced_persona)

    print("EHNANCED DESCRIPTION")

    # Enhance Job Description
    prompt_config = PromptConfig(file_name="jd_ehnancer")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    prompt_template = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", job_description),
        ]
    )

    llm_obj = LLM()
    enhanced_jd = llm_obj.get_response(prompt_template=prompt_template)

    

    # Get the new and updated description for resume combining the enhanced resume and enhanced JD
    prompt_config = PromptConfig(file_name="updated_persona")
    system_prompt = prompt_config.get_prompt(key="system_prompt")

    prompt_template = ChatPromptTemplate(
        [
            ("system", system_prompt),
            (
                "human",
                f"Here is the enhanced job description:\n {enhanced_jd}\n\n Here is a text describing a person:\n {enhanced_persona}",
            ),
        ]
    )

    llm_obj = LLM()
    new_persona = llm_obj.get_response(prompt_template=prompt_template)

    response = get_common_logic(
        enhanced_persona=new_persona,
        template_selected=template_selected,
        bucket_name=bucket_name,
    )

    return response


file_key = "resumes/resume_20251013144653.docx"
template_name = "default"
jd = """
Python + Gen AI

Job Summary

We are seeking a skilled Developer with 5 to 8 years of experience to join our team in a hybrid work model. The ideal candidate will have expertise in Semantic Search Agentic AI and Generative AI. This role involves developing innovative solutions that leverage AI technologies to enhance our products and services. The position offers an opportunity to work in a dynamic environment with a focus on cutting-edge AI applications.

Responsibilities

Develop and implement AI-driven solutions using Semantic Search Agentic AI and Generative AI to improve product functionality and user experience.
Collaborate with cross-functional teams to design and deploy AI models that meet business requirements and enhance operational efficiency.
Conduct thorough testing and validation of AI models to ensure accuracy reliability and performance in real-world scenarios.
Optimize AI algorithms for scalability and integration with existing systems to support seamless deployment and maintenance.
Provide technical expertise and guidance to team members on best practices in AI development and implementation.
Stay updated with the latest advancements in AI technologies and incorporate relevant innovations into ongoing projects.
Analyze and interpret complex data sets to derive actionable insights and drive data-informed decision-making processes.
Document AI development processes methodologies and outcomes to facilitate knowledge sharing and continuous improvement.
Engage in code reviews and provide constructive feedback to peers to maintain high-quality code standards.
Troubleshoot and resolve technical issues related to AI applications to ensure smooth and uninterrupted operation.
Participate in project planning and contribute to the development of project timelines and deliverables.
Communicate effectively with stakeholders to understand project goals and align AI solutions with organizational objectives.
Ensure compliance with data privacy and security regulations in all AI-related activities.
Qualifications

Possess a strong understanding of Semantic Search Agentic AI and Generative AI technologies.
Demonstrate proficiency in programming languages commonly used in AI development such as Python or Java.
Exhibit excellent problem-solving skills and the ability to work independently and collaboratively in a team environment.
Show a track record of successful AI project implementations and the ability to manage multiple projects simultaneously.
Have a keen interest in staying abreast of emerging AI trends and technologies.
Display strong communication skills to effectively convey technical concepts to non-technical stakeholders.
Hold a bachelors degree in computer science engineering or a related field.
Role: Software Development - Other
Industry Type: IT Services & Consulting
Department: Engineering - Software & QA
Employment Type: Full Time, Permanent
Role Category: Software Development
Education
UG: Any Graduate
Key Skills
Skills highlighted with ‘‘ are preferred keyskills
Gen AI Developer
Gen AIPython API
"""

response = job_match(
    file_key=file_key, template_selected=template_name, job_description=jd
)

print(response)
