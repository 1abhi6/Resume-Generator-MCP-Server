from enum import Enum
from pydantic import BaseModel, field_validator


class ResumeTemplate(str, Enum):
    DEFAULT = "default"
    MODERN = "modern"
    CLASSIC = "classic"
    MINIMAL = "minimal"
    CREATIVE = "creative"


class TemplateSelectionInput(BaseModel):
    template_name: str = "default"

    @field_validator("template_name", mode="before")
    def normalize_and_validate_template(cls, v):
        if not isinstance(v, str):
            raise ValueError("Template name must be a string.")

        v = v.strip().lower()

        valid_templates = [t.value for t in ResumeTemplate]
        if v not in valid_templates:
            raise ValueError(
                f"Invalid template '{v}'. Allowed values: {', '.join(valid_templates)}"
            )
        return v


