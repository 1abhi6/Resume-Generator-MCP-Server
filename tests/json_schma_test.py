from pydantic import BaseModel
from typing import List, Optional

class WorkHistoryItem(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str
    details: str

class ContactInfo(BaseModel):
    email: str
    phone: str

class ProfessionalResume(BaseModel):
    name: str
    contact: ContactInfo
    summary: Optional[str] = ""
    competencies: List[str] = []
    work_history: List[WorkHistoryItem] = []

# Generate JSON schema
schema = ProfessionalResume.model_json_schema()
print(schema)
