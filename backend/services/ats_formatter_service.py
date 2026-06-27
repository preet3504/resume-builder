from models.resume import ResumeData, Experience, Education
import re
from typing import List, Optional
from datetime import datetime
from dateutil import parser

class ATSFormatterService:
    """
    Ensures that tailored resume data conforms to ATS-friendly formatting standards.
    This includes chronological ordering, date standardization, and clean lists.
    """

    @classmethod
    def format_resume(cls, resume_data: ResumeData) -> ResumeData:
        """
        Takes a ResumeData object and returns a newly formatted ResumeData object
        that complies with ATS standards.
        """
        formatted_experience = cls._sort_and_format_experience(resume_data.experience)
        formatted_education = cls._sort_and_format_education(resume_data.education)
        formatted_skills = cls._sanitize_list(resume_data.skills)
        
        formatted_achievements = None
        if resume_data.achievements:
            formatted_achievements = cls._sanitize_list(resume_data.achievements)
            
        formatted_summary = None
        if resume_data.summary:
            formatted_summary = resume_data.summary.strip()
            
        formatted_contact_info = cls._format_contact_info(resume_data.contact_info)

        return ResumeData(
            contact_info=formatted_contact_info,
            summary=formatted_summary,
            experience=formatted_experience,
            education=formatted_education,
            skills=formatted_skills,
            achievements=formatted_achievements
        )

    @classmethod
    def _format_contact_info(cls, contact_info: dict) -> dict:
        formatted_info = {}
        for key, value in contact_info.items():
            if isinstance(value, str):
                formatted_info[key] = value.strip()
            else:
                formatted_info[key] = value
        return formatted_info

    @classmethod
    def _parse_date(cls, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        date_str_lower = date_str.lower().strip()
        if date_str_lower in ['present', 'current', 'now']:
            return datetime.now()
        
        try:
            # Parse the date using dateutil
            return parser.parse(date_str)
        except Exception:
            # Fallback for unrecognizable dates
            return None

    @classmethod
    def _standardize_date_str(cls, date_str: Optional[str]) -> str:
        if not date_str:
            return ""
        
        date_str_lower = date_str.lower().strip()
        if date_str_lower in ['present', 'current', 'now']:
            return "Present"
            
        dt = cls._parse_date(date_str)
        if dt:
            # Format as "Month YYYY" (e.g., "January 2020")
            return dt.strftime("%B %Y")
        
        # If parsing fails, return original string cleanly
        return date_str.strip()

    @classmethod
    def _sort_and_format_experience(cls, experiences: List[Experience]) -> List[Experience]:
        formatted_exps = []
        for exp in experiences:
            clean_desc = cls._sanitize_list(exp.description)
            formatted_exp = Experience(
                title=exp.title.strip(),
                company=exp.company.strip(),
                start_date=cls._standardize_date_str(exp.start_date),
                end_date=cls._standardize_date_str(exp.end_date) if exp.end_date else None,
                description=clean_desc
            )
            formatted_exps.append(formatted_exp)
            
        # Sort in reverse chronological order based on start_date
        # If start_date parsing fails, treat it as very old
        def get_sort_key(e: Experience) -> datetime:
            dt = cls._parse_date(e.start_date)
            return dt if dt else datetime.min
            
        formatted_exps.sort(key=get_sort_key, reverse=True)
        return formatted_exps

    @classmethod
    def _sort_and_format_education(cls, education_list: List[Education]) -> List[Education]:
        formatted_edus = []
        for edu in education_list:
            formatted_edu = Education(
                degree=edu.degree.strip(),
                institution=edu.institution.strip(),
                graduation_year=edu.graduation_year.strip(),
                gpa=edu.gpa
            )
            formatted_edus.append(formatted_edu)
            
        # Sort by graduation year descending
        def get_edu_sort_key(e: Education) -> datetime:
            dt = cls._parse_date(e.graduation_year)
            return dt if dt else datetime.min
            
        formatted_edus.sort(key=get_edu_sort_key, reverse=True)
        return formatted_edus

    @classmethod
    def _sanitize_list(cls, items: List[str]) -> List[str]:
        clean_items = []
        for item in items:
            if not isinstance(item, str):
                continue
            # Remove leading bullets (-, *, •) and strip whitespace
            clean_item = re.sub(r'^[\-\*\•\s]+', '', item).strip()
            if clean_item:
                clean_items.append(clean_item)
        return clean_items