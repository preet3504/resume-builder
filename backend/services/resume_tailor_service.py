import logging
from typing import Dict, Any, List
import asyncio

from models.resume import ResumeData, Experience
from models.job_description import JobAnalysisResult
from utils.llm import LLMUtility

logger = logging.getLogger(__name__)

class ResumeTailorService:
    """
    Service to tailor a parsed resume to a specific job description.
    """
    
    @staticmethod
    async def tailor_resume(resume: ResumeData, job_analysis: JobAnalysisResult) -> ResumeData:
        logger.info("Starting resume tailoring process...")
        llm_utility = LLMUtility()
        
        # Convert Pydantic model to dict for easier passing to prompts
        analysis_dict = job_analysis.model_dump()
        
        # 1. Rewrite Summary
        logger.info("Rewriting summary...")
        new_summary_task = llm_utility.rewrite_summary(resume.summary or "", analysis_dict)
        
        # 2. Extract Relevant Skills
        logger.info("Reordering skills...")
        new_skills_task = llm_utility.extract_relevant_skills(resume.skills, analysis_dict)
        
        # 3. Rewrite Experience Bullets
        logger.info("Rewriting experience bullets...")
        exp_tasks = []
        for exp in resume.experience:
            task = llm_utility.rewrite_experience_bullets(
                exp.title, exp.company, exp.description, analysis_dict
            )
            exp_tasks.append(task)
            
        # Execute all LLM calls concurrently
        results = await asyncio.gather(
            new_summary_task,
            new_skills_task,
            *exp_tasks,
            return_exceptions=True
        )
        
        new_summary = results[0] if not isinstance(results[0], Exception) else resume.summary
        if isinstance(results[0], Exception):
             logger.error(f"Summary rewrite failed: {results[0]}")
             
        new_skills = results[1] if not isinstance(results[1], Exception) else resume.skills
        if isinstance(results[1], Exception):
             logger.error(f"Skills rewrite failed: {results[1]}")
        
        # Reconstruct experience list
        new_experiences = []
        for i, exp in enumerate(resume.experience):
            bullets_result = results[i + 2]
            new_bullets = bullets_result if not isinstance(bullets_result, Exception) else exp.description
            if isinstance(bullets_result, Exception):
                 logger.error(f"Experience rewrite failed for {exp.title}: {bullets_result}")
            
            new_experiences.append(
                Experience(
                    title=exp.title,
                    company=exp.company,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                    description=new_bullets
                )
            )
            
        # Create a new tailored ResumeData object
        tailored_resume = ResumeData(
            contact_info=resume.contact_info,
            summary=new_summary,
            experience=new_experiences,
            education=resume.education, # Education usually doesn't need rewriting
            skills=new_skills,
            achievements=resume.achievements
        )
        
        logger.info("Resume tailoring complete.")
        return tailored_resume