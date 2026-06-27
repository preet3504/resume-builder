from pydantic import BaseModel, Field
from typing import List


class JobAnalysisResult(BaseModel):
    # Core Requirements
    required_skills: List[str] = Field(
        default_factory=list,
        description="Must-have technical skills, tools, certifications that are essential for the role"
    )
    preferred_skills: List[str] = Field(
        default_factory=list,
        description="Nice-to-have skills that strengthen candidacy but are not mandatory"
    )
    experience_requirements: str = Field(
        default="",
        description="Years and type of experience required (e.g., '3-5 years in software development', 'Senior level with leadership experience')"
    )
    education_requirements: List[str] = Field(
        default_factory=list,
        description="Required degrees, certifications, educational background (e.g., ['Bachelor\\'s in Computer Science', 'PMP certification'])"
    )

    # Job Details
    job_responsibilities: List[str] = Field(
        default_factory=list,
        description="Key duties and responsibilities of the position as described in the job posting"
    )
    industry_knowledge: List[str] = Field(
        default_factory=list,
        description="Domain-specific knowledge required (e.g., ['Financial regulations', 'Healthcare compliance', 'E-commerce platforms'])"
    )
    technologies_tools: List[str] = Field(
        default_factory=list,
        description="Specific software, platforms, tools, languages, frameworks mentioned in the job description"
    )
    soft_skills: List[str] = Field(
        default_factory=list,
        description="Interpersonal, communication, leadership, and other non-technical skills required for success in the role"
    )