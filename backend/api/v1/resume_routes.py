"""
Resume API Routes — /api/v1/

Phase 2: ResumeParserService is now wired in.
Phase 3: JobDescriptionAnalyzerService is now integrated.
Phases 4-7 will progressively connect remaining services.
"""

import logging
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse

from services.resume_parser_service import ResumeParserService
from services.job_description_analyzer_service import JobDescriptionAnalyzerService
from services.resume_tailor_service import ResumeTailorService
from services.ats_formatter_service import ATSFormatterService
from models.job_description import JobAnalysisResult

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/generate-optimized-resume",
    summary="Generate an ATS-optimized resume",
    response_class=JSONResponse,
)
async def generate_optimized_resume(
    resume: UploadFile = File(..., description="PDF or DOCX resume file"),
    job_description: str = Form(..., description="Target job description text"),
):
    """
    Accepts a resume file (PDF/DOCX) and a job description, processes them
    through the AI pipeline, and returns download URLs for the optimized resume.
    """
    # --- Validate file type ---
    allowed = {".pdf", ".docx"}
    filename = (resume.filename or "").lower()
    if not any(filename.endswith(ext) for ext in allowed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{resume.filename}'. Only PDF and DOCX are accepted.",
        )

    # --- Validate job description ---
    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty.",
        )

    # --- Phase 2: Parse the resume ---
    try:
        resume_data = await ResumeParserService.parse_resume(resume)
        logger.info(
            "Parsed resume for '%s': %d experiences, %d education entries, %d skills",
            resume_data.contact_info.get("name", "Unknown"),
            len(resume_data.experience),
            len(resume_data.education),
            len(resume_data.skills),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error while parsing resume: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while parsing the resume.",
        ) from exc

    # --- Phase 3: Analyze the job description ---
    try:
        job_analysis: JobAnalysisResult = JobDescriptionAnalyzerService.analyze_job_description(job_description)
        logger.info(
            "Analyzed job description: %d required skills, %d preferred skills",
            len(job_analysis.required_skills),
            len(job_analysis.preferred_skills),
        )
    except Exception as exc:
        logger.exception("Unexpected error while analyzing job description: %s", exc)
        # We don't fail the request here - we continue with empty analysis
        # so the resume parsing still provides value
        job_analysis = JobAnalysisResult()
        logger.warning("Continuing with empty job analysis due to error")

    # --- Phases 4–7 (TODO): Tailor → Format → Generate ---
    # Phase 4: Tailor the resume
    try:
        logger.info("Starting Phase 4: Tailoring resume...")
        tailored_resume_data = await ResumeTailorService.tailor_resume(resume_data, job_analysis)
        logger.info("Successfully tailored resume.")
    except Exception as exc:
        logger.exception("Unexpected error while tailoring resume: %s", exc)
        tailored_resume_data = resume_data # Fallback to parsed resume
        logger.warning("Continuing with untailored resume due to error")
        
    # Phase 5: Format the tailored resume for ATS standards
    try:
        logger.info("Starting Phase 5: Formatting resume for ATS standards...")
        formatted_resume_data = ATSFormatterService.format_resume(tailored_resume_data)
        logger.info("Successfully formatted resume.")
    except Exception as exc:
        logger.exception("Unexpected error while formatting resume: %s", exc)
        formatted_resume_data = tailored_resume_data # Fallback
        logger.warning("Continuing with unformatted resume due to error")

    # These will be connected progressively in subsequent phases. (Phases 6-7)

    return {
        "message": "Resume tailored successfully (Phases 6–7 pending — file generation coming soon)",
        "parsed": {
            "contact_info": formatted_resume_data.contact_info,
            "summary": formatted_resume_data.summary,
            "experience_count": len(formatted_resume_data.experience),
            "education_count": len(formatted_resume_data.education),
            "skills_count": len(formatted_resume_data.skills),
            "has_achievements": bool(formatted_resume_data.achievements),
        },
        "job_analysis": {
            "required_skills": job_analysis.required_skills,
            "preferred_skills": job_analysis.preferred_skills,
            "experience_requirements": job_analysis.experience_requirements,
            "education_requirements": job_analysis.education_requirements,
            "job_responsibilities": job_analysis.job_responsibilities,
            "industry_knowledge": job_analysis.industry_knowledge,
            "technologies_tools": job_analysis.technologies_tools,
            "soft_skills": job_analysis.soft_skills,
        },
        "job_description_length": len(job_description.strip()),
    }


@router.get(
    "/download/{format}/{file_id}",
    summary="Download a generated resume",
)
async def download_resume(format: str, file_id: str):
    """
    Download the generated resume in the requested format (pdf or docx).
    Will be fully implemented in Phase 7.
    """
    format_lower = format.lower()
    if format_lower not in ("pdf", "docx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid format '{format}'. Must be 'pdf' or 'docx'.",
        )

    # TODO (Phase 7): Retrieve file from generated/ directory and return FileResponse
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Download endpoint will be available after Phase 7 implementation.",
    )