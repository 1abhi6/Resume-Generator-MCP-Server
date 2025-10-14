from pydantic import BaseModel, Field


class ProcessResumeInput(BaseModel):
    file_key: str = Field(description="S3 File key for AWS")
