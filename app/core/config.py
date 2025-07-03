from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "WellNest API"
    PROJECT_DESCRIPTION: str = "API for WellNest Health Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    HOST: str = "" 
    PORT: int = 8000
    CORS_ORIGINS: list[str] = ["*"]  # Adjust this to your needs

    class Config:
        env_file = ".env"
