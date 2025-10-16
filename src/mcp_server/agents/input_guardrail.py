import os
import re

import textract
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------ INPUT GUARDRAILS --------------


def validate_relevance(text: str) -> bool:
    resume_keywords = [
        "experience",
        "education",
        "skills",
        "project",
        "internship",
        "career",
        "developer",
        "engineer",
        "work",
        "summary",
        "profile",
        "job",
    ]
    if sum(k in text.lower() for k in resume_keywords) >= 3:
        return True

    completion = client.responses.create(
        model="gpt-4o-mini",
        input=f"Is the following text relevant to a resume, job, or professional profile? Answer Yes or No.\n\n{text[:2000]}",
    )
    return "yes" in completion.output_text.lower()


def validate_uploaded_resume(file_path: str) -> bool:
    max_size_mb = 5
    if os.path.getsize(file_path) / (1024 * 1024) > max_size_mb:
        return False

    text = textract.process(file_path).decode("utf-8", errors="ignore")
    if len(text.split()) > 3000:
        return False
    return validate_relevance(text)
