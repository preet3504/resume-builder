# Configuration settings for the ResumeTailor API

import os
from pydantic import model_validator
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
    # Stored as a comma-separated string. pydantic-settings v2 JSON-decodes
    # complex types (set/list) from env, so a plain "set" field would reject
    # a value like ".pdf,.docx". Keep it a str and expose a parsed set below.
    ALLOWED_EXTENSIONS: str = ".pdf,.docx"

    # File storage — defaults for local dev; model_validator overrides to
    # /tmp on Vercel where only /tmp is writable (enforced AFTER env loading
    # so no dashboard env var can accidentally override this).
    UPLOAD_DIR: str = "uploads"
    GENERATED_DIR: str = "generated"

    @model_validator(mode="after")
    def enforce_tmp_on_vercel(self) -> "Settings":
        """
        Vercel serverless functions can only write to /tmp.
        Vercel automatically sets VERCEL=1 at runtime.
        This validator runs after all env-var sources are merged, so it
        unconditionally redirects storage dirs to /tmp — nothing can override it.
        """
        if os.environ.get("VERCEL") == "1":
            self.UPLOAD_DIR = "/tmp/uploads"
            self.GENERATED_DIR = "/tmp/generated"
        return self

    @property
    def allowed_extensions_set(self) -> set[str]:
        """Parsed set of allowed file extensions (e.g. {'.pdf', '.docx'})."""
        return {ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(",") if ext.strip()}

    class Config:
        env_file = ".env"


settings = Settings()


