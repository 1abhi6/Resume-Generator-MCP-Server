from pydantic import BaseModel, HttpUrl

class ValidateURL(BaseModel):
    link: HttpUrl