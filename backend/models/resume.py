from pydantic import BaseModel
from typing import List, Optional

class Experience(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str]

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: str
    gpa: Optional[float] = None

class ResumeData(BaseModel):
    contact_info: dict
    summary: Optional[str] = None
    experience: List[Experience]
    education: List[Education]
    skills: List[str]
    achievements: Optional[List[str]] = None
