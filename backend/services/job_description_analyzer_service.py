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
from langchain.chains import LLMChain
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

        try:
            # Initialize the Groq LLM
            llm = ChatGroq(
                temperature=0.1,  # Low temperature for more consistent extraction
                groq_api_key=os.getenv("GROQ_API_KEY"),
                model_name="llama3-8b-8192"  # Using a fast, capable model
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

            # Create the LLM chain
            chain = LLMChain(llm=llm, prompt=prompt)

            # Run the chain and get the result
            result = chain.run(job_description=job_description)

            # Parse the result into our Pydantic model
            parsed_result = parser.parse(result)

            logger.info("Successfully analyzed job description using LLM")
            return parsed_result

        except Exception as e:
            logger.error(f"Error analyzing job description with LLM: {str(e)}")
            # Fallback to returning a basic result with error information logged
            # In a production system, we might want to return a more structured error
            return JobAnalysisResult(
                required_skills=["Error in analysis"],
                preferred_skills=[],
                experience_requirements="Analysis failed",
                education_requirements=["Analysis failed"],
                job_responsibilities=["Analysis failed"],
                industry_knowledge=["Analysis failed"],
                technologies_tools=["Analysis failed"],
                soft_skills=["Analysis failed"]
            )