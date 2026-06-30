from pydantic import BaseModel
from typing import Dict, List, Optional

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

class Project(BaseModel):
    name: str
    description: List[str]

class ResumeData(BaseModel):
    contact_info: dict
    summary: Optional[str] = None
    experience: List[Experience]
    education: List[Education]
    skills: List[str]
    skill_categories: Optional[Dict[str, List[str]]] = None
    achievements: Optional[List[str]] = None
    projects: List[Project] = []