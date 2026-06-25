# ResumeTailor - ATS Resume Optimizer
## Project Context for Claude Code Sessions

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

#### Backend (FastAPI)
- **Framework**: FastAPI for high-performance async API
- **Endpoints**:
  - `POST /generate-optimized-resume` - accepts PDF/DOCX resume and job description text, returns optimized resume files
  - `GET /download/{format}/{id}` - serves generated resume files (fallback for direct download)
- **Services**:
  - ResumeParserService (PyMuPDF + python-docx)
  - JobDescriptionAnalyzerService (NLP/LLM-based)
  - ResumeTailorService (LLM-powered rewriting and optimization)
  - ATSFormatterService (ensures ATS compliance)
  - ResumeGeneratorService (creates PDF/DOCX outputs)

#### AI Layer
- **Primary Model**: Groq Llama 3.3 70B (for speed) or Hugging Face Llama 3.1/3.3 8B (for privacy)
- **Functions**:
  - Keyword extraction from job descriptions
  - Content rewriting and optimization
  - Relevancy scoring and section prioritization
  - ATS-friendly phrasing suggestions
- **Prompt Engineering**: Carefully crafted prompts for each task to ensure quality outputs

#### Document Processing
- **PDF Processing**: PyMuPDF (fitz) for text extraction with positional information
- **DOCX Processing**: python-docx for structured document parsing
- **PDF Generation**: ReportLab or WeasyPrint for ATS-friendly PDFs
- **DOCX Generation**: python-docx for formatted Word documents

### Data Flow
1. User uploads resume (PDF/DOCX) and enters job description → Frontend sends both to backend `/generate-optimized-resume`
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
- Single API endpoint for resume generation (`/generate-optimized-resume`)
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

### File Structure Reference
```
resume-tailor/
├── src/                    # Frontend Next.js application
│   ├── app/                # App router pages and layouts
│   ├── components/         # Reusable React components
│   ├── lib/                # Utility functions and API clients
│   ├── types/              # TypeScript type definitions
│   └── public/             # Static assets
├── backend/                # Backend FastAPI application
│   ├── main.py             # Application entry point
│   ├── api/                # API route definitions
│   ├── core/               # Configuration and exception handling
│   ├── models/             # Pydantic data models
│   ├── services/           # Business logic services
│   ├── utils/              # Utility functions
│   └── tests/              # Unit and integration tests
├── .env.example            # Frontend environment variables template
├── backend/.env.example    # Backend environment variables template
├── package.json            # Frontend dependencies and scripts
├── requirements.txt        # Backend Python dependencies
└── README.md               # Project overview and setup instructions
```

This CLAUDE.md file should provide complete context for any future Claude Code sessions working on the ResumeTailor project.