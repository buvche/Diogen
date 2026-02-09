from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "Diogen"
    API_V1_STR: str = "/api/v1"
    
    # API Security
    API_KEY: Optional[str] = None  # If not set, auth is disabled (dev mode)

    # Database
    POSTGRES_USER: str = "diogen"
    POSTGRES_PASSWORD: str = "diogen"
    POSTGRES_DB: str = "diogen"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # GitHub Connector
    GITHUB_TOKEN: Optional[str] = None
    
    # Jira Connector
    JIRA_BASE_URL: Optional[str] = None
    JIRA_EMAIL: Optional[str] = None
    JIRA_API_TOKEN: Optional[str] = None

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

settings = Settings()

