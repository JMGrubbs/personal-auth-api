from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class MCPSettings(BaseSettings):
    api_base_url: str = Field(validation_alias="API_BASE_URL")
    timeout: int = Field(default=30, validation_alias="TIMEOUT")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


settings = MCPSettings()