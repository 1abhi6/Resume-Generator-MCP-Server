from src.templates.default.doc_loader import doc
from src.utils import make_link, safe_get

context = {
    "candidate_name": safe_get(response, "name_section", "candidate_name"),
    "phone_number": make_link(
        doc,
        safe_get(response, "contact_details_section", "phone", "text"),
        safe_get(response, "contact_details_section", "phone", "link"),
        underline=True,
        bold=True,
    ),
    "email_address": make_link(
        doc,
        safe_get(response, "contact_details_section", "email", "text"),
        safe_get(response, "contact_details_section", "email", "link"),
        underline=True,
        bold=True,
    ),
    "linkedin_url": make_link(
        doc,
        "LinkedIn",
        safe_get(response, "contact_details_section", "linkedin_url"),
        underline=True,
        bold=True,
    ),
    "github_url": make_link(
        doc,
        "GitHub",
        safe_get(response, "contact_details_section", "github_url"),
        underline=True,
        bold=True,
    ),
    "skills": safe_get(response, "skills_section", "skills") or [],
    "experiences": safe_get(response, "experience_section", "experiences") or [],
    "projects": projects_context,
    "certifications": certifications_context,
    "educations": educations_context,
}
