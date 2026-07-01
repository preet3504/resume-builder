# Configuration settings for the ResumeTailor API

import os
from pydantic_settings import BaseSettings

# Detect Vercel serverless environment (Vercel sets VERCEL=1 automatically)
IS_VERCEL = os.environ.get("VERCEL", "") == "1"

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ResumeTailor"

    # Groq API settings (for Llama 3.3 70B)
    GROQ_API_KEY: str = ""

    # Hugging Face settings (for Llama 3.1/3.3 8B)
    HF_API_TOKEN: str = ""

    # File upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    # Stored as a comma-separated string. pydantic-settings v2 JSON-decodes
    # complex types (set/list) from env, so a plain "set" field would reject
    # a value like ".pdf,.docx". Keep it a str and expose a parsed set below.
    ALLOWED_EXTENSIONS: str = ".pdf,.docx"

    # File storage — use /tmp on Vercel (only writable dir in serverless)
    UPLOAD_DIR: str = "/tmp/uploads" if IS_VERCEL else "uploads"
    GENERATED_DIR: str = "/tmp/generated" if IS_VERCEL else "generated"

    @property
    def allowed_extensions_set(self) -> set[str]:
        """Parsed set of allowed file extensions (e.g. {'.pdf', '.docx'})."""
        return {ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(",") if ext.strip()}

    class Config:
        env_file = ".env"

settings = Settings()

