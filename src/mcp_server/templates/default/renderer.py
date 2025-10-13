"""docxtpl + Jinja2 rendering logic for this template
This module processes default resume sections (projects, certifications, educations, contact info, etc.) and prepares a context dictionary for rendering with docxtpl templates."""

from src.mcp_server.utils import safe_get, make_link


def get_context(doc, response) -> dict:
    """
    Build the context dictionary for docxtpl rendering from the response data.

    Args:
        doc: DocxTemplate document object (used for hyperlinks).
        response: Parsed resume data (usually from Pydantic schema).

    Returns:
        dict: Context dictionary for template rendering.
    """

    # --- Process projects into a list for the template ---
    projects_context = []
    project_section_data = safe_get(response, "project_section", "projects")
    if project_section_data:
        for project in project_section_data:
            # Create a dictionary for each project, including a formatted link
            projects_context.append(
                {
                    "project_name": project.project_name,
                    "points": project.points,
                    "project_link": make_link(
                        doc,
                        text="LINK",
                        url=project.project_link,
                        underline=True,
                        bold=True,
                    ),
                }
            )

    # --- Process certifications into a list for the template ---
    certifications_context = []
    certification_section_data = safe_get(
        response, "certification_section", "certifications"
    )
    if certification_section_data:
        for cert in certification_section_data:
            certifications_context.append(
                {
                    "name": cert.name,
                    "month": cert.month,
                    "year": cert.year,
                    "description": cert.description,
                    "link": make_link(
                        doc, text="LINK", url=cert.link, underline=True, bold=True
                    ),
                }
            )

    # --- Process educations into a list for the template ---
    educations_context = []
    education_section_data = safe_get(response, "education_section", "educations")
    if education_section_data:
        for edu in education_section_data:
            educations_context.append(
                {
                    "degree": edu.degree,
                    "score": edu.score,
                    "institution": edu.institution,
                    "start_month": edu.start_month,
                    "start_year": edu.start_year,
                    "end_month": edu.end_month,
                    "end_year": edu.end_year,
                }
            )

    # --- Safely extract all values into the final context ---
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

    return context
