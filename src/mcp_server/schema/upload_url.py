from pydantic import BaseModel, field_validator, Field

from src.mcp_server.utils import VALID_FILE_TYPES


class UploadURLInput(BaseModel):
    file_type: str = Field(..., description="File type of the URL. Only PDF, DOCX, PNG, JPG, or JPEG allowed.")

    @field_validator("file_type")
    def validate_file_type(cls, v):
        if v.lower() not in VALID_FILE_TYPES:
            raise ValueError(
                "Invalid file type. Only PDF, DOCX, PNG, JPG, or JPEG allowed."
            )
        return v.lower()


class UploadURLResponse(BaseModel):
    upload_url: str
    file_key: str
