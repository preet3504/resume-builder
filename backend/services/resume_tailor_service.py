import logging
from typing import Dict, Any, List, Optional
import asyncio

from models.resume import ResumeData, Experience
from models.job_description import JobAnalysisResult
from utils.llm import LLMUtility

logger = logging.getLogger(__name__)


async def _noop():
    return None


class ResumeTailorService:
    """Service to tailor a parsed resume to a specific job description."""

    @staticmethod
    async def tailor_resume(resume: ResumeData, job_analysis: JobAnalysisResult) -> ResumeData:
        logger.info("Starting resume tailoring process...")
        llm_utility = LLMUtility()

        analysis_dict = job_analysis.model_dump()

        # 1. Rewrite Summary
        logger.info("Rewriting summary...")
        new_summary_task = llm_utility.rewrite_summary(resume.summary or "", analysis_dict)

        # 2. Reorder skills (flat list)
        logger.info("Reordering skills...")
        new_skills_task = llm_utility.extract_relevant_skills(resume.skills, analysis_dict)

        # 2b. Reorder skill categories (if original resume had them)
        new_categories_task = (
            llm_utility.reorder_skill_categories(resume.skill_categories, analysis_dict)
            if resume.skill_categories
            else _noop()
        )

        # 3. Rewrite Experience Bullets
        logger.info("Rewriting experience bullets...")
        exp_tasks = [
            llm_utility.rewrite_experience_bullets(
                exp.title, exp.company, exp.description, analysis_dict
            )
            for exp in resume.experience
        ]

        # Execute all LLM calls concurrently
        results = await asyncio.gather(
            new_summary_task,
            new_skills_task,
            new_categories_task,
            *exp_tasks,
            return_exceptions=True,
        )

        new_summary = results[0] if not isinstance(results[0], Exception) else resume.summary
        if isinstance(results[0], Exception):
            logger.error(f"Summary rewrite failed: {results[0]}")

        new_skills = results[1] if not isinstance(results[1], Exception) else resume.skills
        if isinstance(results[1], Exception):
            logger.error(f"Skills rewrite failed: {results[1]}")

        new_categories = results[2] if not isinstance(results[2], Exception) else resume.skill_categories
        if isinstance(results[2], Exception):
            logger.error(f"Skill categories reorder failed: {results[2]}")

        # Reconstruct experience list (results offset by 3 now)
        new_experiences = []
        for i, exp in enumerate(resume.experience):
            bullets_result = results[i + 3]
            new_bullets = bullets_result if not isinstance(bullets_result, Exception) else exp.description
            if isinstance(bullets_result, Exception):
                logger.error(f"Experience rewrite failed for {exp.title}: {bullets_result}")
            new_experiences.append(
                Experience(
                    title=exp.title,
                    company=exp.company,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                    description=new_bullets,
                )
            )

        tailored_resume = ResumeData(
            contact_info=resume.contact_info,
            summary=new_summary,
            experience=new_experiences,
            education=resume.education,
            skills=new_skills,
            skill_categories=new_categories,
            achievements=resume.achievements,
            projects=resume.projects,  # preserve projects through tailoring
        )

        logger.info("Resume tailoring complete.")
        return tailored_resume