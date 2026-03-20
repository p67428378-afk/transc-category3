from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@db:5432/transactions_db"
    LLM_API_KEY: str = "your_llm_api_key"

    class Config:
        env_file = ".env"

settings = Settings()
