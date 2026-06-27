"""
Resume API Routes — /api/v1/

Phase 2: ResumeParserService is now wired in.
Phases 3-7 will progressively connect remaining services.
"""

import logging
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse

from services.resume_parser_service import ResumeParserService

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

    Current Phase 2 behaviour:
    - Validates file type
    - Parses the resume into structured ResumeData
    - Returns parsed data as confirmation (full pipeline wired in Phase 7)
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

    # --- Phases 3–7 (TODO): Analyze JD → Tailor → Format → Generate ---
    # These will be connected progressively in subsequent phases.

    return {
        "message": "Resume parsed successfully (Phases 3–7 pending — full pipeline coming soon)",
        "parsed": {
            "contact_info": resume_data.contact_info,
            "summary": resume_data.summary,
            "experience_count": len(resume_data.experience),
            "education_count": len(resume_data.education),
            "skills_count": len(resume_data.skills),
            "has_achievements": bool(resume_data.achievements),
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
