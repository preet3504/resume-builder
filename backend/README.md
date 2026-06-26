# ResumeTailor Backend

This is the backend for the ResumeTailor application, built with FastAPI.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source .venv/bin/activate
     ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root of the backend directory and add the following:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   HF_API_TOKEN=your_huggingface_api_token_here
   ```

5. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

## Project Structure

- `main.py`: Entry point of the FastAPI application.
- `api/v1/`: API route definitions.
- `core/`: Configuration settings.
- `models/`: Pydantic data models.
- `services/`: Business logic services.
- `utils/`: Utility functions.
- `tests/`: Unit and integration tests.

## API Endpoints

- `POST /api/v1/generate-optimized-resume`: Generate an optimized resume based on a job description.
- `GET /api/v1/download/{format}/{file_id}`: Download the generated resume in PDF or DOCX format.

## Dependencies

- FastAPI
- PyMuPDF (fitz)
- python-docx
- groq
- huggingface_hub
- pydantic
- python-dotenv
- langchain
- langchain-community
- langchain-groq
- langchain-text-splitters

See `requirements.txt` for the exact versions.

## Environment Variables

- `GROQ_API_KEY`: API key for Groq (used for Llama 3.3 70B model).
- `HF_API_TOKEN`: API token for Hugging Face (used for Llama 3.1/3.3 8B model).

These API keys are used by both the direct API clients and LangChain integrations.

## LangChain Integration

The backend uses LangChain for LLM orchestration, providing:
- Standardized interface to LLMs (Groq and Hugging Face)
- Prompt templating and management
- Chains for resume processing workflows
- Output parsing and validation

This abstraction allows for easy switching between different LLM providers and enhances maintainability.

These API keys are used by both the direct API clients and LangChain integrations.

## Notes

- The backend is designed to be stateless and does not store user data permanently.
- Uploaded files are temporarily stored and deleted after processing.