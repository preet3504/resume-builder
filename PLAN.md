# Backend Implementation Plan for ResumeTailor

## Overview
This plan outlines the phased implementation of the backend for the ResumeTailor ATS resume optimizer. Each phase is designed to be completed, tested, and verified before moving to the next. After each phase, the CLAUDE.md file will be updated to reflect the current state.

## Phase 1: Dependency and Environment Setup
**Goal**: Ensure the backend environment is ready with all necessary dependencies and directory structure.

### Tasks:
1. Review and update `backend/requirements.txt` with the latest compatible versions:
   - fastapi
   - uvicorn[standard]
   - pydantic
   - pydantic-settings
   - PyMuPDF
   - python-docx
   - reportlab (for PDF generation, as Weasyprint was removed due to Windows compatibility)
   - groq (for Groq API)
   - huggingface-hub (for Hugging Face API)
   - python-multipart (for handling file uploads)
   - langchain (for LLM framework and utilities)
   - langchain-community (for community integrations)
   - langchain-groq (for Groq integration)
   - langchain-text-splitters (for text processing)
2. Install dependencies in the backend virtual environment.
3. Create necessary directories for file handling:
   - `backend/uploads` (for temporary storage of uploaded resumes)
   - `backend/generated` (for storing generated resumes before download)
4. Verify the environment by running a simple FastAPI test (e.g., `uvicorn backend.main:app --reload`).

### Success Criteria:
- All dependencies install without errors.
- The FastAPI server starts successfully and responds to the root endpoint.
- Directories `uploads` and `generated` exist and are writable.

### Update CLAUDE.md:
After completing this phase, update the "Current State" section in CLAUDE.md to reflect the completed setup.

## Phase 2: Implement ResumeParserService
**Goal**: Enable robust parsing of PDF and DOCX resumes into structured `ResumeData`.

### Tasks:
1. Implement PDF parsing using PyMuPDF (`fitz`):
   - Extract text with positional information to help identify sections.
   - Use heuristics or layout analysis to identify contact information, summary, experience, education, skills, and achievements.
   - Parse experience entries: job title, company, start/end dates, and description bullet points.
   - Parse education entries: degree, institution, graduation year, GPA.
   - Extract skills as a list of strings.
   - Extract achievements as a list of strings (if present).
2. Implement DOCX parsing using python-docx:
   - Similar extraction logic as for PDF, leveraging document structure (paragraphs, styles).
3. Handle edge cases: missing sections, varied formatting, etc.
4. Return a fully populated `ResumeData` object (or raise appropriate exceptions if parsing fails).

### Success Criteria:
- The service can parse a variety of sample PDF and DOCX resumes into accurate `ResumeData` objects.
- Unit tests demonstrate correct extraction for common resume formats.

### Update CLAUDE.md:
Update the "Current State" section to note that resume parsing is functional.

## Phase 3: Implement JobDescriptionAnalyzerService
**Goal**: Analyze job descriptions to extract relevant keywords, skills, qualifications, and responsibilities.

### Tasks:
1. Implement text preprocessing: remove extra whitespace, convert to lowercase for matching, etc.
2. Implement keyword extraction:
   - Use a combination of regex patterns and NLP techniques (e.g., noun phrase extraction) to identify hard skills, tools, certifications.
   - Optionally, leverage the LLM (Groq or Hugging Face) for more accurate extraction (to be implemented in Phase 4's AI utility).
3. Extract required qualifications (e.g., degrees, years of experience).
4. Extract responsibilities and key activities.
5. Return a structured object (e.g., a dictionary or a Pydantic model) containing:
   - `keywords`: list of important terms
   - `required_skills`: list of skills
   - `qualifications`: list of qualifications
   - `responsibilities`: list of responsibilities
   - `industry_terminology`: list of industry-specific terms

### Success Criteria:
- The service accurately extracts key information from various job descriptions.
- Unit tests show correct extraction for sample job descriptions.

### Update CLAUDE.md:
Update the "Current State" section to note that job description analysis is functional.

## Phase 4: Implement LLM Utility and ResumeTailorService
**Goal**: Create a reusable LLM interaction utility and use it to tailor resumes based on job descriptions.

### Tasks:
1. Create an LLM utility in `backend/utils/llm.py`:
   - Built using LangChain framework for LLM orchestration
   - Support for both Groq (Llama 3.3 70B) and Hugging Face (Llama 3.1/3.3 8B) APIs via LangChain integrations
   - Functions for:
     - Keyword extraction from text (to be used by JobDescriptionAnalyzerService if LLM-based)
     - Rewriting text to align with given keywords and tone
     - Scoring relevance of resume sections to job description
     - Generating ATS-friendly phrasing suggestions
   - Include error handling, retry logic, and fallback mechanisms
   - Utilize LangChain prompt templates for consistent, high-quality outputs
2. Implement ResumeTailorService:
   - Take parsed resume data and analyzed job description as input.
   - Use the LLM utility to:
     - Identify which keywords from the job description should be incorporated into the resume.
     - Rewrite the professional summary to better match the job.
     - Rewrite experience bullet points to highlight relevant achievements and use action verbs.
     - Score each experience/education/skills section for relevance.
     - Optionally, reorder sections to highlight the most relevant content.
   - Ensure that the tailoring remains truthful and does not fabricate experience.
   - Output a tailored `ResumeData` object.

### Success Criteria:
- The LLM utility (built with LangChain) can successfully communicate with both Groq and Hugging Face APIs (with API keys configured).
- The ResumeTailorService produces tailored resumes that maintain original facts while improving relevance to the job description.
- Unit tests (with mocked LLM responses) verify the tailoring logic.

### Update CLAUDE.md:
Update the "Current State" section to note that AI-powered tailoring is functional.

## Phase 5: Implement ATSFormatterService
**Goal**: Ensure the tailored resume data conforms to ATS-friendly formatting standards.

### Tasks:
1. Define ATS-friendly formatting rules:
   - Use standard sections: Contact Info, Summary, Experience, Education, Skills, Achievements (if applicable).
   - Ensure chronological order for experience (most recent first).
   - Ensure bullet points are used for descriptions (no paragraphs).
   - Remove any complex structures (tables, columns, graphics, headers/footers) - though these should already be absent from parsed data.
   - Standardize date formats (e.g., "YYYY-MM" or "Month YYYY").
   - Ensure skills are listed as a simple, comma-separated or bullet-point list.
2. Implement methods in ATSFormatterService to:
   - Validate and reorder resume data according to the rules.
   - Convert experience descriptions to bullet points if they are not already.
   - Ensure contact info is in a standard format.
   - Return a formatted `ResumeData` object ready for generation.

### Success Criteria:
- The service takes any `ResumeData` and outputs an ATS-compliant version.
- Unit tests verify that the output meets the defined ATS rules.

### Update CLAUDE.md:
Update the "Current State" section to note that ATS formatting is functional.

## Phase 6: Implement ResumeGeneratorService
**Goal**: Generate PDF and DOCX files from tailored resume data.

### Tasks:
1. PDF Generation:
   - Use reportlab to create a PDF with ATS-friendly styling:
     - Fonts: Arial, Calibri, or Helvetica (or reportlab's default fonts that are similar).
     - Standard section headings (bold, slightly larger font).
     - Bullet points for experience descriptions.
     - Appropriate spacing and margins.
     - No tables, columns, or graphics.
   - Implement a function that takes `ResumeData` and returns a PDF file (or bytes).
2. DOCX Generation:
   - Use python-docx to create a DOCX with similar ATS-friendly styling.
   - Ensure the document uses standard Word styles (Normal, Heading 1, Heading 2) for ATS compatibility.
   - Implement a function that takes `ResumeData` and returns a DOCX file (or bytes).
3. Handle file saving: save generated files to the `backend/generated` directory with a unique identifier (e.g., UUID).

### Success Criteria:
- Generated PDF and DOCX files are valid and open correctly.
- The content matches the input `ResumeData`.
- The formatting is clean, ATS-friendly, and free of tables/columns/graphics.

### Update CLAUDE.md:
Update the "Current State" section to note that resume generation is functional.

## Phase 7: Update API Routes and Implement File Handling
**Goal**: Connect the API endpoints to the implemented services and handle file uploads/downloads.

### Tasks:
1. Modify `backend/api/v1/resume_routes.py`:
   - In `generate_optimized_resume`:
     - Validate uploaded file type (PDF/DOCX) and size.
     - Save the uploaded file temporarily to `backend/uploads`.
     - Use ResumeParserService to parse the resume.
     - Use JobDescriptionAnalyzerService to analyze the job description.
     - Use ResumeTailorService to tailor the resume.
     - Use ATSFormatterService to ensure ATS compliance.
     - Use ResumeGeneratorService to generate PDF and DOCX files.
     - Save the generated files to `backend/generated` with a unique ID.
     - Return a JSON response containing the file ID and a message.
   - In `download_resume`:
     - Validate the format (pdf or docx) and file ID.
     - Retrieve the corresponding file from `backend/generated`.
     - Return the file as a `FileResponse` or `StreamingResponse`.
2. Implement file cleanup mechanism (optional): delete old generated files after a certain time to prevent disk space issues.
3. Add error handling throughout: return appropriate HTTP status codes and user-friendly messages.

### Success Criteria:
- The endpoint `/api/v1/generate-optimized-resume` accepts a resume file and job description, processes them, and returns a file ID.
- The endpoint `/api/v1/download/{format}/{file_id}` serves the generated file in the requested format.
- The generated files are correct and ATS-friendly.
- Error cases (invalid file type, too large, missing data) return appropriate error responses.

### Update CLAUDE.md:
Update the "Current State" section to note that the API endpoints are functional.

## Phase 8: Error Handling, Validation, and Testing
**Goal**: Ensure the backend is robust, handles errors gracefully, and has been thoroughly tested.

### Tasks:
1. Implement comprehensive error handling in all services and API routes:
   - Catch exceptions and return HTTP 4xx or 500 errors with meaningful messages.
   - Validate inputs at every stage.
2. Add file type and size validation in the API route.
3. Implement logging for key steps and errors.
4. Write integration tests that test the full flow:
   - Upload a sample resume, provide a job description, generate optimized resume, download and verify content.
5. Test edge cases: empty job description, corrupted PDF/DOCX, missing sections in resume, etc.
6. Ensure that the latest within