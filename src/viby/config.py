from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Config(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = [
            ".env",
            str(Path.home() / ".config" / "viby" / ".env"),
        ]
        env_file_encoding = "utf-8"

# Try to load config, but don't fail if not found
try:
    config = Config()
except Exception:
    # Will be handled by CLI setup
    config = None