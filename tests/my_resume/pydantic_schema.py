from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import List, Optional
import re


# Name Section
class NameSection(BaseModel):
    candidate_name: Optional[str] = Field(
        None, description="Full name of the candidate, automatically capitalized"
    )

    @field_validator("candidate_name")
    def capitalize_name(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return v.title()  # e.g., 'abhishek gupta' → 'Abhishek Gupta'
        return v


# Contact Detail Section
class LinkTextPair(BaseModel):
    text: Optional[str] = Field(None, description="Phone Number or Email to be shown in the document")
    link: Optional[str] = Field(None, description="Clickable hyperlink (tel:, mailto:)")

    @field_validator("link")
    def validate_link(cls, v):
        if not v:
            return v  # Allow None
        if v.startswith("tel:"):
            if not re.match(r"^tel:\+?[0-9]{7,15}$", v):
                raise ValueError(
                    "Invalid phone link format. Expected format: tel:+919876543210"
                )
        elif v.startswith("mailto:"):
            if not re.match(
                r"^mailto:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", v
            ):
                raise ValueError(
                    "Invalid mailto link format. Expected format: mailto:example@email.com"
                )
        else:
            raise ValueError("Link must start with tel:, mailto:")
        return v


class ContactDetails(BaseModel):
    phone: Optional[LinkTextPair] = None
    email: Optional[LinkTextPair] = None
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub profile URL")


# Skill Section
class SkillItem(BaseModel):
    category: Optional[str] = Field(
        None,
        description="Skill category name, e.g., 'Programming Languages, AI & LLM Tools'",
    )
    items: Optional[List[str]] = Field(
        None, description="List of individual skills under this category"
    )


class SkillsSection(BaseModel):
    skills: Optional[List[SkillItem]] = Field(
        None, description="List of categorized skill groups"
    )


# Final Unified Resume Schema
class ResumeSchema(BaseModel):
    name_section: Optional[NameSection] = None
    contact_details_section: Optional[ContactDetails] = None
    skills_section: Optional[SkillsSection] = None
