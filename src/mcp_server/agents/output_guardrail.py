import os

import textract
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def is_safe_output(text: str) -> bool:
    banned_words = ["sexual", "violence", "hate", "terror", "nsfw"]
    if any(bad in text.lower() for bad in banned_words):
        return False
    moderation = client.moderations.create(model="omni-moderation-latest", input=text)
    return not moderation.results[0].flagged


def check_grammar_and_tone(text: str) -> bool:
    completion = client.responses.create(
        model="gpt-4o-mini",
        input=f"Is this text grammatically correct and professional in tone? Answer Yes or No.\n\n{text[:3000]}",
    )
    return "yes" in completion.output_text.lower()


def check_resume_structure(text: str) -> bool:
    sections = ["education", "experience", "skills", "projects", "summary"]
    return sum(sec in text.lower() for sec in sections) >= 2


def validate_output_resume(text: str) -> bool:
    return (
        is_safe_output(text)
        and check_grammar_and_tone(text)
        and check_resume_structure(text)
    )
