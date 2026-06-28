"""
Resume API Routes — /api/v1/

Phase 2: ResumeParserService is now wired in.
Phase 3: JobDescriptionAnalyzerService is now integrated.
Phase 4: ResumeTailorService is now wired in.
Phase 5: ATSFormatterService is now wired in.
Phase 6: ResumeGeneratorService is now wired in.
Phase 7: Download endpoint implemented.
"""

import logging
import os
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse

from services.resume_parser_service import ResumeParserService
from services.job_description_analyzer_service import JobDescriptionAnalyzerService
from services.resume_tailor_service import ResumeTailorService
from services.ats_formatter_service import ATSFormatterService
from services.resume_generator_service import ResumeGeneratorService
from models.job_description import JobAnalysisResult
from core.config import settings

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
    through the AI pipeline, and returns file IDs for the generated PDF and DOCX resumes.
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
    # The AI analysis is core to this product. If it fails we must NOT pretend
    # the request succeeded — surface a clear error to the user instead.
    try:
        job_analysis: JobAnalysisResult = JobDescriptionAnalyzerService.analyze_job_description(job_description)
        logger.info(
            "Analyzed job description: %d required skills, %d preferred skills",
            len(job_analysis.required_skills),
            len(job_analysis.preferred_skills),
        )
    except Exception as exc:
        logger.exception("Error while analyzing job description: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to analyze the job description. The AI service may be "
                   "unavailable or misconfigured (check GROQ_API_KEY).",
        ) from exc

    # --- Phase 4: Tailor the resume ---
    try:
        logger.info("Starting Phase 4: Tailoring resume...")
        tailored_resume_data = await ResumeTailorService.tailor_resume(resume_data, job_analysis)
        logger.info("Successfully tailored resume.")
    except Exception as exc:
        logger.exception("Error while tailoring resume: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to optimize the resume. The AI service may be "
                   "unavailable or misconfigured (check GROQ_API_KEY).",
        ) from exc

    # --- Phase 5: Format the tailored resume for ATS standards ---
    try:
        logger.info("Starting Phase 5: Formatting resume for ATS standards...")
        formatted_resume_data = ATSFormatterService.format_resume(tailored_resume_data)
        logger.info("Successfully formatted resume.")
    except Exception as exc:
        logger.exception("Error while formatting resume: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while formatting the resume.",
        ) from exc

    # --- Phase 6: Generate PDF and DOCX files ---
    try:
        logger.info("Starting Phase 6: Generating PDF and DOCX resumes...")
        pdf_path = ResumeGeneratorService.generate_pdf(formatted_resume_data)
        docx_path = ResumeGeneratorService.generate_docx(formatted_resume_data)
        logger.info("Successfully generated PDF and DOCX resumes.")

        # Extract file IDs from the paths (format: "generated/<uuid>.ext")
        pdf_file_id = os.path.splitext(os.path.basename(pdf_path))[0]
        docx_file_id = os.path.splitext(os.path.basename(docx_path))[0]
    except Exception as exc:
        logger.exception("Unexpected error while generating resume files: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the resume files.",
        ) from exc

    # Return the file IDs for download
    return {
        "message": "Resume optimized and generated successfully",
        "pdf_file_id": pdf_file_id,
        "docx_file_id": docx_file_id,
    }


@router.get(
    "/download/{format}/{file_id}",
    summary="Download a generated resume",
)
async def download_resume(format: str, file_id: str):
    """
    Download the generated resume in the requested format (pdf or docx).
    """
    format_lower = format.lower()
    if format_lower not in ("pdf", "docx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid format '{format}'. Must be 'pdf' or 'docx'.",
        )

    # Construct the expected file path
    filename = f"{file_id}.{format_lower}"
    file_path = os.path.join(settings.GENERATED_DIR, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found for format '{format}' and ID '{file_id}'.",
        )

    # Return the file as a response
    return FileResponse(
        path=file_path,
        media_type=f'application/{format_lower}',
        filename=filename
    )