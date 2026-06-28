import os
import logging
from typing import List, Dict, Any
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

    async def extract_relevant_skills(self, current_skills: List[str], job_analysis: Dict[str, Any]) -> List[str]:
        if not current_skills:
            return []
            
        parser = CommaSeparatedListOutputParser()
        
        prompt_template = """
        You are an expert ATS optimizer. Filter and reorder the candidate's existing skills to prioritize those most relevant to the target job.
        Include ALL original skills, but put the most relevant ones first.
        Do NOT add any skills that the candidate does not already have in their list.
        
        Candidate's Original Skills:
        {current_skills}
        
        Target Job Requirements:
        {required_skills}
        
        {format_instructions}
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["current_skills", "required_skills"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm
        
        try:
            result = await chain.ainvoke({
                "current_skills": ", ".join(current_skills),
                "required_skills": ", ".join(job_analysis.get("required_skills", []))
            })
            
            sorted_skills = parser.parse(result.content)
            return [s.strip() for s in sorted_skills if s.strip()]
        except Exception as e:
            logger.error(f"Error extracting relevant skills: {e}")
            return current_skills
