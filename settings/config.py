from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

env_from = Path(".") / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_from)
    
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
settings = Settings()