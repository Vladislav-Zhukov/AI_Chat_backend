from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AI Chat Backend"

    DATABASE_URL: str
    REDIS_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    AI_PROVIDER: str = "mock"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = ""

    AI_CONTEXT_MESSAGES_LIMIT: int = 20

    RATE_LIMIT_MESSAGES: int = 20
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file= ".env",
        extra="ignore",
    )

settings = Settings()