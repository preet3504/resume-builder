# Configuration settings for the ResumeTailor API

import os
from pydantic_settings import BaseSettings

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
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx"}

    # File storage
    UPLOAD_DIR: str = "uploads"
    GENERATED_DIR: str = "generated"

    class Config:
        env_file = ".env"

settings = Settings()
