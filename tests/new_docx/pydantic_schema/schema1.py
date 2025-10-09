from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class LinkModel(BaseModel):
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    portfolio_website: Optional[HttpUrl] = None


class ResumeData(BaseModel):
    name: str
    age: int
    gender: str
    qualification: str
    projects: List[str]
    links: Optional[LinkModel] = None
