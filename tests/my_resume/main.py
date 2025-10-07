# from pydantic_schema import ResumeSchema
from docxtpl import DocxTemplate, RichText
import json

# schema_dict = ResumeSchema.model_json_schema()
# print(schema_dict)


# Prepare RichText links
def make_link(doc, text: str, url: str, underline=False):
    if not url:
        return ""
    rt = RichText()
    rt.add(text, url_id=doc.build_url_id(url), underline=underline)
    return rt


doc = DocxTemplate("test1.docx")

dummy_structure = {
    "name_section": {"candidate_name": "John Doe"},
    "contact_details_section": {
        "phone": {"text": "+1-555-1234", "link": "tel:+1-555-1234"},
        "email": {"text": "johndoe@email.com", "link": "mailto:johndoe@email.com"},
        "linkedin_url": "https://www.linkedin.com/in/johndoe",
        "github_url": "https://github.com/johndoe",
    },
    "skills_section": {
        "skills": [
            {
                "category": "Programming Languages",
                "items": ["Python", "JavaScript", "Java"],
            },
            {"category": "AI & LLM Tools", "items": ["TensorFlow", "OpenAI GPT"]},
            {"category": "Web Development", "items": ["HTML", "CSS", "React"]},
        ]
    },
}


context = {
    "candidate_name": dummy_structure["name_section"]["candidate_name"],
    "phone_number": make_link(
        doc,
        dummy_structure["contact_details_section"]["phone"]["text"],
        dummy_structure["contact_details_section"]["phone"]["link"],
        underline=True,
    ),
    "email_address": make_link(
        doc,
        dummy_structure["contact_details_section"]["email"]["text"],
        dummy_structure["contact_details_section"]["email"]["link"],
        underline=True,
    ),
    "linkedin_url": make_link(
        doc,
        "LinkedIn",
        dummy_structure["contact_details_section"]["linkedin_url"],
        underline=True,
    ),
    "github_url": make_link(
        doc,
        "GitHub",
        dummy_structure["contact_details_section"]["github_url"],
        underline=True,
    ),
    "skills": dummy_structure["skills_section"]["skills"],
}

print(context)

doc.render(context)
doc.save("generated_test1.docx")
