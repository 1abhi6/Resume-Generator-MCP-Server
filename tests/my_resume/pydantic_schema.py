from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import re
from datetime import datetime

now = datetime.now()


# -----------------------------
# Name Section
# -----------------------------
class NameSection(BaseModel):
    candidate_name: Optional[str] = Field(
        None, description="Full name of the candidate, automatically Upper Case"
    )

    @field_validator("candidate_name")
    def capitalize_name(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return v.upper()
        return v


# -----------------------------
# Contact Details Section
# -----------------------------
class LinkTextPair(BaseModel):
    text: Optional[str] = Field(
        None, description="Phone Number or Email to be shown in the document"
    )
    link: Optional[str] = Field(None, description="Clickable hyperlink (tel:, mailto:)")

    @field_validator("link")
    def validate_link(cls, v):
        if not v:
            return v  # Allow None
        if v.startswith("tel:"):
            if not re.match(r"^tel:\+?[0-9]{7,15}$", v):
                raise ValueError(
                    "Invalid phone link format. Expected: tel:+919876543210"
                )
        elif v.startswith("mailto:"):
            if not re.match(
                r"^mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", v
            ):
                raise ValueError("Invalid mailto link format.")
        else:
            raise ValueError("Link must start with tel:, mailto:")
        return v


class ContactDetails(BaseModel):
    phone: Optional[LinkTextPair] = None
    email: Optional[LinkTextPair] = None
    linkedin_url: Optional[str] = Field(
        None, description="LinkedIn profile URL starting with http or https"
    )
    github_url: Optional[str] = Field(
        None, description="GitHub profile URL starting with http or https"
    )

    @field_validator("linkedin_url", "github_url")
    def validate_url(cls, v):
        if not v:
            return v
        if not re.match(r"^https?://[A-Za-z0-9._%+-]+(?:/[A-Za-z0-9._%+-]*)*$", v):
            raise ValueError("Invalid URL format. Must start with http:// or https://")
        return v


# -----------------------------
# Skills Section
# -----------------------------
class SkillItem(BaseModel):
    category: Optional[str] = None
    items: Optional[List[str]] = None


class SkillsSection(BaseModel):
    skills: Optional[List[SkillItem]] = None


# -----------------------------
# Experience Section
# -----------------------------
class Experience(BaseModel):
    """Represents one complete work experience entry."""

    job_role: str = Field(..., description="Job title or position held.")
    company_name: str = Field(..., description="Company or organization name.")
    city: str = Field(..., description="City where the company is located.")
    country: str = Field(..., description="Country where the company is located.")
    start_month: str = Field(
        now.strftime("%b"), description="Joining month, e.g., 'Nov'."
    )
    start_year: str = Field(
        now.strftime("%Y"), description="Joining year, e.g., '2023'."
    )
    end_month: Optional[str] = Field(
        now.strftime("%b"), description="Leaving month, e.g., 'Aug'."
    )
    end_year: Optional[str] = Field(
        now.strftime("%Y"), description="Leaving year, e.g., '2025'."
    )
    points: List[str] = Field(
        ...,
        description="List of up to 4 bullet points describing key achievements or responsibilities.",
        max_length=85,
    )

    @field_validator("points")
    def validate_points_length(cls, v):
        if len(v) > 4:
            raise ValueError("Each experience can have a maximum of 4 bullet points.")
        return v


class ExperienceSection(BaseModel):
    """Container for all work experiences in a resume."""

    experiences: List[Experience] = Field(
        ..., description="List of work experiences with details and bullet points."
    )


# -----------------------------
# Project Section
# -----------------------------
class Project(BaseModel):
    """Represents one project entry."""

    project_name: str = Field(..., description="The official name of the project.")
    project_link: Optional[str] = Field(
        None, description="A valid URL to the project (e.g., GitHub, live demo)."
    )
    points: List[str] = Field(
        ...,
        description="List of bullet points describing the project's features or impact max 4 points",
    )

    @field_validator("project_link")
    def validate_project_url(cls, v):
        if not v:
            return v
        # Simple regex for http/https URLs
        if not re.match(r"^https?://[^\s/$.?#].[^\s]*$", v):
            raise ValueError("Invalid URL format. Must start with http:// or https://")
        return v


class ProjectSection(BaseModel):
    """Container for all projects in a resume."""

    projects: List[Project] = Field(
        ..., description="A list of the candidate's projects."
    )


# -----------------------------
# Certification Section
# -----------------------------
class Certification(BaseModel):
    """Represents one certification entry."""

    name: str = Field(..., description="The full name of the certification.")
    link: Optional[str] = Field(
        "None", description="A verifiable URL for the certificate."
    )
    month: str = Field(
        now.strftime("%b"),
        description="The month the certification was obtained, e.g., 'Sept'.",
    )
    year: str = Field(
        now.strftime("%Y"),
        description="The year the certification was obtained, e.g., '2025'.",
    )
    description: str = Field(
        ...,
        description="A brief, one-line description of the certification's focus.",
        max_length=70,
    )

    @field_validator("link")
    def validate_cert_url(cls, v):
        if not v:
            return v
        if not re.match(r"^https?://[^\s/$.?#].[^\s]*$", v):
            raise ValueError("Invalid URL format. Must start with http:// or https://")
        return v


class CertificationSection(BaseModel):
    """Container for all certifications."""

    certifications: List[Certification] = Field(
        ..., description="A list of the candidate's certifications."
    )

# -----------------------------
# Education Section (NEW)
# -----------------------------
class Education(BaseModel):
    """Represents one educational qualification."""

    degree: str = Field(
        ...,
        description="The name of the degree or examination (e.g., 'Bachelor of Science in IT').",
    )
    score: str = Field(
        ...,
        description="The score obtained, including the format (e.g., '8.1 CGPA', '80%').",
    )
    institution: str = Field(
        ..., description="The full name and location of the institution."
    )
    start_month: Optional[str] = Field(
        None, description="The starting month, e.g., 'Apr'."
    )
    start_year: Optional[str] = Field(
        None, description="The starting year, e.g., '2021'."
    )
    end_month: str = Field(..., description="The ending/completion month, e.g., 'Apr'.")
    end_year: str = Field(..., description="The ending/completion year, e.g., '2025'.")


class EducationSection(BaseModel):
    """Container for all educational qualifications."""

    educations: List[Education] = Field(
        ..., description="A list of the candidate's educational qualifications."
    )


# -----------------------------
# Final Unified Resume Schema
# -----------------------------
class ResumeSchema(BaseModel):
    name_section: Optional[NameSection] = None
    contact_details_section: Optional[ContactDetails] = None
    skills_section: Optional[SkillsSection] = None
    experience_section: Optional[ExperienceSection] = None
    project_section: Optional[ProjectSection] = None
    certification_section: Optional[CertificationSection] = None
    education_section: Optional[EducationSection] = None

