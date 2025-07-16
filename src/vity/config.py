from pydantic_settings import BaseSettings
from pathlib import Path

class Config(BaseSettings):
    vity_llm_api_key: str
    vity_llm_base_url: str
    vity_llm_model: str
    vity_terminal_history_limit: int  = 1000
    class Config:
        env_file = [
            f for f in [
            ".env",
            str(Path.home() / ".config" / "vity" / ".env"),
        ] if Path(f).exists()]
        env_file_encoding = "utf-8"
        
        

# Try to load config, but don't fail if not found
try:
    config = Config()
except Exception as e:
    print(e)
    config = None