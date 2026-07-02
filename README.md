# ResumeTailor - ATS Resume Optimizer

**🚀 Live Application:** [https://resume-builder-five-eta-85.vercel.app/](https://resume-builder-five-eta-85.vercel.app/)

## Project Overview

ResumeTailor is an intelligent, AI-powered web application designed to help job seekers create highly optimized, Applicant Tracking System (ATS) friendly resumes. By taking an existing resume and a target job description, the system intelligently analyzes both inputs and generates a professionally tailored resume that highlights the most relevant skills, experiences, and achievements.

### Key Features
*   **Dual Format Support:** Upload and parse existing resumes in both PDF and DOCX formats.
*   **AI-Powered Tailoring:** Utilizes advanced LLMs (Groq Llama 3.3 70B / Hugging Face Llama 3.1 8B) to perform keyword optimization, content rewriting, and relevancy scoring based on the provided job description.
*   **ATS Optimization:** Generates clean, easily parsable documents with standard fonts, chronologically ordered sections, and proper formatting, free of complex tables or graphics.
*   **Instant Export:** Download the optimized resume in both PDF and DOCX formats with a single click.

## Prerequisites

Ensure you have the following installed before proceeding:
*   **Node.js:** v18 or higher (for the frontend)
*   **Python:** v3.10 or higher (for the backend)
*   **npm** or **yarn** (for frontend package management)
*   **pip** (for backend package management)

## Installation Instructions

The project is split into two main directories: `frontend` (Next.js) and `backend` (FastAPI).

### 1. Clone the Repository
```bash
git clone <repository-url>
cd resume-builder
```

### 2. Backend Setup
```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install Node dependencies
npm install
```

## Configuration Requirements

The backend relies on environment variables for API keys and operational settings.

1.  Navigate to the `backend` directory.
2.  Copy the provided example environment file:
    ```bash
    cp .env.example .env
    ```
3.  Open the `.env` file and configure the necessary variables:
    ```env
    # Backend Environment Variables
    API_V1_STR=/api/v1
    PROJECT_NAME=ResumeTailor
    
    # Groq API settings (Required for LLM processing)
    GROQ_API_KEY=your_groq_api_key_here
    
    # Hugging Face settings (Optional, if using HF models)
    HF_API_TOKEN=your_huggingface_api_token_here
    
    # File upload settings
    MAX_UPLOAD_SIZE=10485760  # 10 MB
    ALLOWED_EXTENSIONS=.pdf,.docx
    
    # File storage directories
    UPLOAD_DIR=uploads
    GENERATED_DIR=generated
    ```

*Note: Ensure you have a valid Groq API key for the AI tailoring services to function properly.*

## Usage Guidelines

To run the application locally, you need to start both the backend and frontend development servers.

### Starting the Backend
From the `backend` directory, with your virtual environment activated:
```bash
uvicorn main:app --reload
```
The backend API will be available at `http://localhost:8000`.

### Starting the Frontend
From the `frontend` directory:
```bash
npm run dev
```
The web interface will be available at `http://localhost:3000`.

### Using the Application
1.  Open `http://localhost:3000` in your web browser.
2.  Upload your current resume (PDF or DOCX format) using the drag-and-drop interface or file selector.
3.  Paste the target job description into the designated text area.
4.  Click the "Generate Optimized Resume" button.
5.  Wait for the AI to process and optimize the content (typically under 8 seconds).
6.  Use the provided buttons to download your newly optimized ATS-friendly resume in PDF or DOCX format.

## API Documentation

The FastAPI backend provides automated interactive documentation. Once the backend server is running, you can view the detailed API specification at:
*   **Swagger UI:** `http://localhost:8000/docs`
*   **ReDoc:** `http://localhost:8000/redoc`

### Primary Endpoints

#### `POST /api/v1/generate-optimized-resume`
Accepts a PDF or DOCX resume file and a job description text string. Processes the inputs through the AI tailoring pipeline and returns identifiers for the optimized files.

#### `GET /api/v1/download/{format}/{id}`
Serves the generated optimized resume file for download.
*   `format`: `pdf` or `docx`
*   `id`: The unique file identifier returned by the generation endpoint.

## Contribution Guidelines

We welcome contributions to improve ResumeTailor. To contribute:
1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request describing your changes.

Please ensure any new features or significant changes are documented in the `CLAUDE.md` context file to maintain accurate project state. Adhere to existing code styles and include appropriate error handling for new API integrations.

## License

This project is open-source. Please see the `LICENSE` file in the root directory for full details. (If no license file exists, standard copyright applies).
