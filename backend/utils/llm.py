import os
import re
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
load_dotenv()

class BulletsOutput(BaseModel):
    bullets: List[str] = Field(description="List of rewritten bullet points")

class LLMUtility:
    """
    Utility class for interacting with Language Models via LangChain.
    Handles rewriting and tailoring of resume content.
    """
    def __init__(self):
        # We will use llama-3.3-70b-versatile for complex rewriting
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. Set it in backend/.env to enable AI tailoring."
            )

        self.llm = ChatGroq(
            temperature=0.2, 
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile"
        )
        
    async def rewrite_summary(self, current_summary: str, job_analysis: Dict[str, Any]) -> str:
        if not current_summary:
            return ""
            
        prompt_template = """
        You are an expert resume writer. Rewrite the following professional summary to highlight the candidate's relevance to the target job.
        Do NOT fabricate any information. Only emphasize the skills and experiences that align with the job requirements.
        
        Original Summary:
        {current_summary}
        
        Target Job Details:
        Required Skills: {required_skills}
        Experience Requirements: {experience_requirements}
        Responsibilities: {job_responsibilities}
        
        Return ONLY the rewritten summary as plain text without any introductory phrases or quotes.
        """
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["current_summary", "required_skills", "experience_requirements", "job_responsibilities"]
        )
        chain = prompt | self.llm
        
        try:
            result = await chain.ainvoke({
                "current_summary": current_summary,
                "required_skills": ", ".join(job_analysis.get("required_skills", [])),
                "experience_requirements": job_analysis.get("experience_requirements", ""),
                "job_responsibilities": ", ".join(job_analysis.get("job_responsibilities", []))
            })
            return result.content.strip(' "')
        except Exception as e:
            logger.error(f"Error rewriting summary: {e}")
            return current_summary

    async def rewrite_experience_bullets(self, title: str, company: str, bullets: List[str], job_analysis: Dict[str, Any]) -> List[str]:
        if not bullets:
            return []
            
        parser = PydanticOutputParser(pydantic_object=BulletsOutput)
        
        prompt_template = """
        You are an expert resume writer. Rewrite the following experience bullet points for a '{title}' at '{company}' to better align with the target job.
        
        Rules:
        1. Keep the same number of bullet points, or combine them if it makes sense. Do not fabricate any new accomplishments.
        2. Use strong action verbs.
        3. Incorporate relevant ATS keywords from the target job where factually accurate.
        4. Focus on quantifiable metrics if they exist in the original bullets.
        
        Original Bullets:
        {bullets}
        
        Target Job Keywords/Skills:
        {required_skills}
        
        {format_instructions}
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["title", "company", "bullets", "required_skills"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm
        
        try:
            result = await chain.ainvoke({
                "title": title,
                "company": company,
                "bullets": "\n".join([f"- {b}" for b in bullets]),
                "required_skills": ", ".join(job_analysis.get("required_skills", []))
            })
            
            parsed = parser.parse(result.content)
            return parsed.bullets
        except Exception as e:
            logger.error(f"Error rewriting experience bullets: {e}")
            return bullets

    @staticmethod
    def _is_valid_skill(s: str) -> bool:
        """Reject entries that look like sentences rather than skill names."""
        s = s.strip()
        if not s or len(s) < 2:
            return False
        # Too long to be a skill name
        if len(s) > 60:
            return False
        # Contains a period mid-string — likely a sentence fragment
        if re.search(r'\.\s+[A-Z]', s) or (s.count('.') > 1):
            return False
        # More than 8 words is almost certainly a sentence
        if len(s.split()) > 8:
            return False
        return True

    async def extract_relevant_skills(self, current_skills: List[str], job_analysis: Dict[str, Any]) -> List[str]:
        if not current_skills:
            return []

        prompt_template = """You are an ATS resume optimizer. Reorder the candidate's skills to put the most job-relevant ones first.

STRICT RULES — violating any rule makes your response unusable:
1. Output ONLY a comma-separated list of skill names. Nothing else.
2. Include EVERY skill from the original list — do not drop or add any.
3. Do NOT write explanations, reasoning, notes, or any text besides the skill names.
4. Do NOT repeat the list. Output it exactly once.

Candidate's skills:
{current_skills}

Target job required skills (for relevance ranking only):
{required_skills}

Your entire response must be exactly: skill1, skill2, skill3, ..."""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["current_skills", "required_skills"],
        )

        chain = prompt | self.llm

        try:
            result = await chain.ainvoke({
                "current_skills": ", ".join(current_skills),
                "required_skills": ", ".join(job_analysis.get("required_skills", [])),
            })
            raw = result.content.strip()

            # Strip any leading label like "Reordered list:" or "Skills:" the LLM may add
            raw = re.sub(r"^[^:]{0,40}:\s*", "", raw, count=1)

            # Split on commas; keep only entries that look like actual skill names
            candidates = [s.strip() for s in raw.split(",")]
            valid = [s for s in candidates if self._is_valid_skill(s)]

            if not valid:
                return current_skills

            # Fall back to original for any that got lost (safety net)
            original_lower = {s.lower() for s in current_skills}
            result_lower = {s.lower() for s in valid}
            missing = [s for s in current_skills if s.lower() not in result_lower]
            return valid + missing
        except Exception as e:
            logger.error(f"Error extracting relevant skills: {e}")
            return current_skills

    async def reorder_skill_categories(
        self, skill_categories: Dict[str, List[str]], job_analysis: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Reorder the skill category dict so the most job-relevant categories appear first.
        Skills within each category are preserved as-is.
        """
        if not skill_categories or len(skill_categories) <= 1:
            return skill_categories

        category_names = list(skill_categories.keys())

        prompt_template = """You are an ATS resume optimizer. Reorder these skill category names so the most relevant categories for the target job appear first.

STRICT RULES:
1. Output ONLY a comma-separated list of the category names. Nothing else.
2. Include EVERY category name from the original list.
3. Do NOT write explanations, reasoning, or any extra text.

Skill categories:
{categories}

Target job required skills (for relevance ranking only):
{required_skills}

Your entire response must be exactly: Category1, Category2, Category3, ..."""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["categories", "required_skills"],
        )

        chain = prompt | self.llm

        try:
            result = await chain.ainvoke({
                "categories": ", ".join(category_names),
                "required_skills": ", ".join(job_analysis.get("required_skills", [])),
            })
            raw = result.content.strip()
            raw = re.sub(r"^[^:]{0,40}:\s*", "", raw, count=1)

            ordered_names = [s.strip() for s in raw.split(",") if s.strip()]
            # Build reordered dict; add any missing categories at the end
            reordered: Dict[str, List[str]] = {}
            seen = set()
            for name in ordered_names:
                # Case-insensitive match back to original key
                match = next((k for k in category_names if k.lower() == name.lower()), None)
                if match and match not in seen:
                    reordered[match] = skill_categories[match]
                    seen.add(match)
            for k in category_names:
                if k not in seen:
                    reordered[k] = skill_categories[k]
            return reordered
        except Exception as e:
            logger.error(f"Error reordering skill categories: {e}")
            return skill_categories
