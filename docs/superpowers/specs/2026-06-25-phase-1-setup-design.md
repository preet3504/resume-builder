# Phase 1 Project Setup Design - ResumeTailor

## Overview
This document outlines the file structure and setup approach for Phase 1 of the ResumeTailor project, focusing on creating a solid foundation for both frontend (Next.js) and backend (FastAPI) applications with proper separation of concerns.

## Directory Structure
```
resume-tailor/
├── backend/                 # FastAPI backend
│   ├── app/                 # Main application package
│   │   ├── __init__.py
│   │   ├── main.py          # Application entry point
│   │   ├── core/            # Configuration and exception handling
│   │   │   ├── __init__.py
│   │   │   ├── config.py    # Environment variable management
│   │   │   └── exceptions.py # Custom exception handlers
│   │   ├── api/             # API route definitions
│   │   │   ├── __init__.py
│   │   │   ├── v1/          # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py # API router configuration
│   │   │   │   └── endpoints/
│   │   │   │       ├── __init__.py
│   │   │   │       └── resume.py # Resume generation endpoints
│   │   ├── services/        # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── resume_parser.py
│   │   │   ├── job_description_analyzer.py
│   │   │   ├── resume_tailor.py
│   │   │   ├── ats_formatter.py
│   │   │   └── resume_generator.py
│   │   ├── models/          # Pydantic data models
│   │   │   ├── __init__.py
│   │   │   ├── resume.py
│   │   │   ├── job_description.py
│   │   │   └── generation_response.py
│   │   └── utils/           # Utility functions
│   │       ├── __init__.py
│   │       ├── file_handlers.py
│   │       ├── llm_client.py
│   │       └── prompts.py
│   ├── tests/               # Test files
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/                # Next.js frontend (using app router)
│   ├── src/
│   │   ├── app/             # App router pages and layouts
│   │   │   ├── layout.tsx   # Root layout with global styles
│   │   │   ├── page.tsx     # Main page with upload and input components
│   │   │   └── globals.css  # Global stylesheet
│   │   ├── components/      # Reusable React components
│   │   │   ├── ResumeUpload.tsx
│   │   │   ├── JobDescriptionInput.tsx
│   │   │   ├── GenerateButton.tsx
│   │   │   ├── ProcessingStatus.tsx
│   │   │   └── DownloadButtons.tsx
│   │   ├── lib/             # Utility functions and API clients
│   │   │   ├── api.ts       # API client functions
│   │   │   └── utils.ts     # Utility functions
│   │   ├── types/           # TypeScript type definitions
│   │   │   ├── resume.ts
│   │   │   ├── jobDescription.ts
│   │   │   └── apiResponse.ts
│   │   └── public/          # Static assets
│   ├── package.json         # Frontend dependencies and scripts
│   ├── next.config.js       # Next.js configuration
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   ├── postcss.config.js    # PostCSS configuration
│   └── tsconfig.json        # TypeScript configuration
├── .gitignore               # Git ignore rules
├── README.md                # Project overview and setup instructions
└── .env.example             # Frontend environment variables template
```

## Key Design Decisions

### 1. Frontend-Backend Separation
- Complete separation of concerns with dedicated folders
- Frontend uses Next.js 13+ with App Router for modern React patterns
- Backend uses FastAPI for high-performance async API development

### 2. Configuration Management
- Environment variables managed through python-dotenv (backend) and NEXT_PUBLIC_ variables (frontend)
- Separate .env.example files for each end
- Centralized configuration in backend/app/core/config.py

### 3. Dependency Management
- Updated to current stable versions for better security and features
- Frontend: Next.js 13.5.0, React 18.2.0, Tailwind CSS 3.3.3, TypeScript 5.1.6
- Backend: FastAPI 0.104.0, Uvicorn 0.24.0, Pydantic 2.5.0

### 4. Code Organization
- Feature-based organization within backend/app/
- Clear separation of concerns: routes, services, models, utils
- TypeScript interfaces for frontend-backend communication
- Proper module structure with __init__.py files for Python packages

### 5. Development Experience
- Separate development servers for frontend and backend
- Hot reloading configured for both sides
- Clear README with setup instructions
- Comprehensive .gitignore to exclude unnecessary files

## Technical Constraints Addressed
- ✅ Support PDF and DOCX upload/output formats
- ✅ Single API endpoint for resume generation (/generate-optimized-resume)
- ✅ Processing time under 8 seconds target
- ✅ No permanent storage of user data (temporary files only)
- ✅ File type and size validation for security
- ✅ Environment variables for API keys and configuration
- ✅ Responsive web interface
- ✅ ATS-friendly formatting (standard fonts, no tables/columns/graphics)

## Next Steps
Upon approval of this design, the implementation plan will be created using the writing-plans skill, detailing the exact steps to create this file structure and initialize the project.