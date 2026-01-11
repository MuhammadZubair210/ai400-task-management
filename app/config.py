from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./taskmanagement.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
