from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = ""
    
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []

    class Config:
        # Load from .env file, checking both current and parent directory
        env_file = (".env", "../.env")
        env_file_encoding = "utf-8"
        case_sensitive = True

try:
    settings = Settings()
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"WARNING: Failed to load settings from .env: {e}")
    raise
