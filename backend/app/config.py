from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # This will load DATABASE_URL from our .env file automatically
    database_url: str = "postgresql+asyncpg://postgres:password@db:5432/sharebridge"
    secret_key: str = "super-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
