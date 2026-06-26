# ResumeTailor - ATS Resume Optimizer
## Project Context for Claude Code Sessions

### Hard Rule
**Always update this CLAUDE.md file whenever new functionality is added, significant changes are made, or important project details change.** This ensures the context remains accurate for all future sessions.

### Project Overview
ResumeTailor is an intelligent, AI-powered web application that helps job seekers create highly optimized, ATS-friendly resumes tailored to specific job descriptions. Users upload their existing resume and provide a target job description, and the system generates a new, professional resume optimized for Applicant Tracking Systems.

### Core Functionality

#### 1. Input Handling
- **Resume Upload**: Support for PDF and DOCX formats
  - PDF parsing using PyMuPDF
  - DOCX parsing using python-docx
  - Extract structured information: experience, skills, education, achievements, contact info
- **Job Description Input**: Text input field for users to paste job descriptions
  - Parse to extract: required skills, qualifications, responsibilities, keywords, industry terminology

#### 2. AI-Powered Resume Tailoring
- **Keyword Optimization**: 
  - Extract important keywords from job description (hard skills, tools, certifications, soft skills, industry jargon)
  - Strategically incorporate keywords into resume without keyword stuffing
  - Maintain natural language flow
- **Content Rewriting**:
  - Rephrase bullet points and summaries to align with job language and priorities
  - Preserve/enhance quantified achievements where possible
  - Use action verbs and impact-focused language
- **Relevancy Scoring**:
  - Score each experience/skill section based on relevance to job description
  - Highlight most relevant experiences/skills
  - De-emphasize or shorten less relevant content (while maintaining truthfulness)

#### 3. ATS Optimization
- **Formatting**:
  - Use standard, ATS-friendly fonts (Arial, Calibri, Helvetica)
  - Clean, simple formatting without tables, columns, graphics, headers/footers
  - Proper section headings (Experience, Skills, Education, etc.)
  - Chronological order where appropriate
  - Standard bullet points and spacing
- **File Generation**:
  - Output formats: PDF and DOCX
  - One-click download functionality

#### 4. User Experience
- Simple, intuitive interface
- Clear upload areas for resume and job description
- Real-time processing indicators
- Clear download buttons for both formats
- Responsive design for mobile/desktop

### Technical Architecture

#### Frontend (Next.js)
- **Framework**: Next.js 13+ with App Router
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React hooks/context
- **Components**:
  - ResumeUpload component (handles PDF/DOCX upload)
  - JobDescriptionInput component (textarea for job description)
  - GenerateButton component (triggers optimization process)
  - ProcessingStatus component (spinner/progress indicator)
  - DownloadButtons component (PDF/DOCX download buttons)
- **Additional**:
  - Custom hooks (useApi, useFormState) in lib/
  - API utility in lib/api.ts

#### Backend (FastAPI)
- **Framework**: FastAPI for high-performance async API
- **Endpoints**:
  - `POST /api/v1/generate-optimized-resume` - accepts PDF/DOCX resume and job description text, returns optimized resume files
  - `GET /api/v1/download/{format}/{id}` - serves generated resume files (fallback for direct download)
- **Services**:
  - ResumeParserService (PyMuPDF + python-docx)
  - JobDescriptionAnalyzerService (NLP/LLM-based)
  - ResumeTailorService (LLM-powered rewriting and optimization)
  - ATSFormatterService (ensures ATS compliance)
  - ResumeGeneratorService (creates PDF/DOCX outputs)
- **Additional**:
  - Configuration management via pydantic Settings
  - Data models (Experience, Education, ResumeData)
  - Utility functions for file handling

#### AI Layer
- **Primary Model**: Groq Llama 3.3 70B (for speed) or Hugging Face Llama 3.1/3.3 8B (for privacy)
- **Framework**: LangChain for LLM orchestration and prompt management
- **Functions**:
  - Keyword extraction from job descriptions
  - Content rewriting and optimization
  - Relevancy scoring and section prioritization
  - ATS-friendly phrasing suggestions
- **Prompt Engineering**: Carefully crafted prompts for each task to ensure quality outputs using LangChain prompt templates

#### Document Processing
- **PDF Processing**: PyMuPDF (fitz) for text extraction with positional information
- **DOCX Processing**: python-docx for structured document parsing
- **PDF Generation**: ReportLab or WeasyPrint for ATS-friendly PDFs
- **DOCX Generation**: python-docx for formatted Word documents

### Data Flow
1. User uploads resume (PDF/DOCX) and enters job description → Frontend sends both to backend `/api/v1/generate-optimized-resume`
2. Backend extracts resume data and analyzes job description → Processes with LLM to optimize resume
3. Backend generates PDF/DOCX files → Returns download URLs or streams files directly
4. Frontend shows download buttons → User downloads preferred format (PDF and/or DOCX)

### Key Constraints & Boundaries

#### In Scope:
- Resume upload (PDF/DOCX)
- Job description text input
- AI-powered resume tailoring and optimization via single generate endpoint
- ATS-friendly PDF/DOCX generation
- One-click download (after generate)
- Responsive web interface

#### Out of Scope:
- User accounts/authentication
- Resume storage/history
- Direct job application integration
- Video/resume multimedia elements
- Non-English language support (initial version)
- Complex design templates (to maintain ATS compatibility)

#### Technical Constraints:
- Support PDF and DOCX upload formats
- Support PDF and DOCX output formats
- Single API endpoint for resume generation (`/api/v1/generate-optimized-resume`)
- Processing time under 8 seconds for typical resumes
- No permanent storage of user data (temporary files only)
- File type validation for security
- Size limits to prevent DoS attacks
- Environment variables for API keys
- Responsive web interface
- ATS-friendly formatting (standard fonts, no tables/columns/graphics)

### Success Metrics
- User completion rate (upload + job description → generate → download)
- Processing time under 8 seconds for typical resumes
- ATS compatibility validation (testing with common ATS systems)
- User satisfaction surveys
- Reduction in job application rejection rates (qualitative feedback)

### Current State (as of this session)
- **Implementation Status**: Initial project structure created with frontend and backend stubs. Backend dependencies updated: removed weasyprint (due to Windows compatibility) and removed version specifiers for flexibility. Fixed pydantic BaseSettings import to use pydantic-settings package. Added LangChain dependencies for LLM orchestration. **Phase 1 complete: Dependencies updated and installed, upload/generated directories created and added to .gitignore.**
- **Files Present**: 
  - Design specifications: `docs/superpowers/specs/2026-06-25-resume-tailor-design.md`
  - Frontend: Next.js app with components, hooks, and page structure (`frontend/app/`, `frontend/components/`, `frontend/lib/`)
  - Backend: FastAPI app with API routes, config, models, services, and utilities (`backend/main.py`, `backend/api/`, `backend/core/`, `backend/models/`, `backend/services/`, `backend/utils/`)
  - Environment templates: `backend/.env.example`
  - Dependency files: `frontend/package.json`, `backend/requirements.txt`
  - Directories: `backend/uploads/`, `backend/generated/` (added to .gitignore)
- **Git Status**: 
  - Last commit added design documents and CLAUDE.md.
  - Current branch: `main` (up to date with origin/main).
  - Recent changes include project structure setup, initial component/backend stubs, dependency updates (including LangChain), configuration fix, and Phase 1 backend setup (dependencies, directories, .gitignore).

### How to Use This CLAUDE.md
This file serves as the single source of truth for project context in every new Claude Code session. It should be read at the start of each session to understand:
1. The overall project goals and boundaries
2. What has been implemented so far (to avoid rework)
3. What remains to be built
4. Technical constraints and success criteria

When starting a new task, refer to the "Current State" and "In Scope"/"Out of Scope" sections to ensure alignment with project goals.
Remember the **Hard Rule**: Always update this file when new functionality is added or important changes occur.