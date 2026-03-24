from pydantic_settings import BaseSettings, SettingsConfigDict

class MCPSettings(BaseSettings):
    api_base_url: str = "http://database-managment-api:8000/api/v1"
    timeout: int = 30

    model_config = SettingsConfigDict(env_file=".env")

settings = MCPSettings()