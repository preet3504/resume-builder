"""
JobDescriptionAnalyzerService — Phase 3 Implementation

Analyzes job description text to extract structured information for resume optimization.
Uses LangChain with Groq LLM for intelligent extraction.
"""

from typing import List
from models.job_description import JobAnalysisResult
import logging
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class JobDescriptionAnalyzerService:
    """
    Analyzes job description text to extract structured information.

    Uses LangChain with Groq LLM to intelligently parse job descriptions
    and identify key requirements, skills, responsibilities, and qualifications.
    """

    @staticmethod
    def analyze_job_description(job_description: str) -> JobAnalysisResult:
        """
        Analyze a job description and extract structured information.

        Args:
            job_description: Raw job description text

        Returns:
            JobAnalysisResult: Structured analysis of the job description
        """
        # Handle empty or None input
        if not job_description or not job_description.strip():
            logger.warning("Received empty job description")
            return JobAnalysisResult()

        # Fail fast (and clearly) if the AI service is not configured.
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. Set it in backend/.env to enable AI analysis."
            )

        try:
            # Initialize the Groq LLM
            llm = ChatGroq(
                temperature=0.1,  # Low temperature for more consistent extraction
                groq_api_key=api_key,
                model_name="llama-3.1-8b-instant"  # Fast, currently-supported Groq model
            )

            # Set up the Pydantic output parser
            parser = PydanticOutputParser(pydantic_object=JobAnalysisResult)

            # Create the prompt template
            prompt_template = """
            You are an expert HR analyst and technical recruiter. Your task is to analyze job descriptions
            and extract structured information that can be used to optimize resumes.

            Extract the following information from the job description provided below:
            - required_skills: Must-have technical skills, tools, certifications that are essential for the role
            - preferred_skills: Nice-to-have skills that strengthen candidacy but are not mandatory
            - experience_requirements: Years and type of experience required (e.g., '3-5 years in software development')
            - education_requirements: Required degrees, certifications, educational background
            - job_responsibilities: Key duties and responsibilities of the position
            - industry_knowledge: Domain-specific knowledge required (e.g., financial regulations, healthcare compliance)
            - technologies_tools: Specific software, platforms, tools, languages, frameworks mentioned
            - soft_skills: Interpersonal, communication, leadership, and other non-technical skills required

            Job Description:
            {job_description}

            {format_instructions}
            """

            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["job_description"],
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )

            # Build the chain using the modern LCEL syntax (prompt | llm | parser).
            # The parser runs as part of the chain and returns a JobAnalysisResult.
            chain = prompt | llm | parser

            parsed_result: JobAnalysisResult = chain.invoke(
                {"job_description": job_description}
            )

            logger.info("Successfully analyzed job description using LLM")
            return parsed_result

        except Exception as e:
            # Do NOT swallow the error and return placeholder data — that would
            # let the request masquerade as a success. Surface it so the caller
            # can return a proper error response to the user.
            logger.error(f"Error analyzing job description with LLM: {str(e)}")
            raise RuntimeError(f"Job description analysis failed: {e}") from e