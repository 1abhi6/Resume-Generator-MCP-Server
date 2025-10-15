from pydantic import BaseModel
from src.mcp_server.templates import DefaultResumeSchema, ModernResumeSchema


def get_schema(template_name: str) -> BaseModel:
    schema_dict = {"default": DefaultResumeSchema, "modern": ModernResumeSchema}

    template_schema = schema_dict.get(template_name, None)

    if template_schema is not None:
        return template_schema

    raise ValueError("Invalid template name. Can be only `default`, `modern`")
