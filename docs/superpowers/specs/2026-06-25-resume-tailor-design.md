# ResumeTailor - ATS Resume Optimizer Design Specification

## Project Overview
ResumeTailor is an intelligent, AI-powered web application that helps job seekers create highly optimized, ATS-friendly resumes tailored to specific job descriptions. Users upload their existing resume and provide a target job description, and the system generates a new, professional resume optimized for Applicant Tracking Systems.

## Core Functionality

### 1. Input Handling
- **Resume Upload**: Support for PDF and DOCX formats
  - PDF parsing using PyMuPDF
  - DOCX parsing using python-docx
  - Extract structured information: experience, skills, education, achievements, contact info
- **Job Description Input**: Text input field for users to paste job descriptions
  - Parse to extract: required skills, qualifications, responsibilities, keywords, industry terminology

### 2. AI-Powered Resume Tailoring
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

### 3. ATS Optimization
- **Formatting**:
  - Use standard, ATS-friendly fonts (Arial, Calibri, Helvetica)
  - Clean, simple formatting without tables, columns, graphics, headers/footers
  - Proper section headings (Experience, Skills, Education, etc.)
  - Chronological order where appropriate
  - Standard bullet points and spacing
- **File Generation**:
  - Output formats: PDF and DOCX
  - One-click download functionality

### 4. User Experience
- Simple, intuitive interface
- Clear upload areas for resume and job description
- Real-time processing indicators
- Clear download buttons for both formats
- Responsive design for mobile/desktop

## Technical Architecture

### Frontend (Next.js)
- **Framework**: Next.js 13+ with App Router
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React hooks/context
- **Components**:
  - ResumeUpload component (handles PDF/DOCX upload)
  - JobDescriptionInput component (textarea for job description)
  - GenerateButton component (triggers optimization process)
  - ProcessingStatus component (spinner/progress indicator)
  - DownloadButtons component (PDF/DOCX download buttons)

### Backend (FastAPI)
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

### AI Layer
- **Primary Model**: Groq Llama 3.3 70B (for speed) or Hugging Face Llama 3.1/3.3 8B (for privacy)
- **Framework**: LangChain for LLM orchestration and prompt management
- **Functions**:
  - Keyword extraction from job descriptions
  - Content rewriting and optimization
  - Relevancy scoring and section prioritization
  - ATS-friendly phrasing suggestions
- **Prompt Engineering**: Carefully crafted prompts for each task to ensure quality outputs using LangChain prompt templates

### Document Processing
- **PDF Processing**: PyMuPDF (fitz) for text extraction with positional information
- **DOCX Processing**: python-docx for structured document parsing
- **PDF Generation**: ReportLab or WeasyPrint for ATS-friendly PDFs
- **DOCX Generation**: python-docx for formatted Word documents

## Data Flow
1. User uploads resume (PDF/DOCX) and enters job description → Frontend sends both to backend `/generate-optimized-resume`
2. Backend extracts resume data and analyzes job description → Processes with LLM to optimize resume
3. Backend generates PDF/DOCX files → Returns download URLs or streams files directly
4. Frontend shows download buttons → User downloads preferred format (PDF and/or DOCX)

## Error Handling & Validation
- File type validation (only PDF/DOCX accepted)
- File size limits (reasonable limits for resume documents)
- Text extraction fallbacks for problematic PDFs
- API error handling with user-friendly messages
- Processing timeouts with retry mechanisms
- Empty/invalid job description handling
- Privacy: Temporary file storage with automatic cleanup

## Testing Strategy
- **Unit Tests**: 
  - Resume parsing accuracy with various PDF/DOCX formats
  - Job description keyword extraction accuracy
  - LLM prompt effectiveness testing
  - ATS formatting compliance checks
- **Integration Tests**:
  - End-to-end resume upload → analysis → tailoring → generation flow
  - API endpoint validation
  - File generation and download tests
- **Manual Testing**:
  - Various resume formats and designs
  - Different job description styles and industries
  - ATS compatibility verification (using common ATS systems if available)

## Security & Privacy Considerations
- No permanent storage of user resumes or job data
- Temporary file storage with automatic cleanup (e.g., after 1 hour)
- File type validation to prevent malicious uploads
- Size limits to prevent DoS attacks
- Environment variables for API keys and sensitive configuration
- Secure file handling practices

## Performance Considerations
- Asynchronous processing for LLM calls
- Efficient file streaming for large documents
- Caching of frequent job description keywords (if appropriate)
- Optimized prompts to minimize LLM token usage
- Background file cleanup processes

## Future Enhancements
- LinkedIn profile import
- Multiple job description targeting
- Cover letter generation
- ATS score prediction/feedback
- Template selection (while maintaining ATS compatibility)
- Integration with job boards/APIs

## Project Boundaries
**In Scope**:
- Resume upload (PDF/DOCX)
- Job description text input
- AI-powered resume tailoring and optimization via single generate endpoint
- ATS-friendly PDF/DOCX generation
- One-click download (after generate)
- Responsive web interface

**Out of Scope**:
- User accounts/authentication
- Resume storage/history
- Direct job application integration
- Video/resume multimedia elements
- Non-English language support (initial version)
- Complex design templates (to maintain ATS compatibility)

## Success Metrics
- User completion rate (upload + job description → generate → download)
- Processing time under 8 seconds for typical resumes (faster due to single API call)
- ATS compatibility validation (testing with common ATS systems)
- User satisfaction surveys
- Reduction in job application rejection rates (qualitative feedback)