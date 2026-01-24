from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Postgres Connection URL
    POSTGRES_URL: str

    APP_ENV: str = "development"

    SECRET_KEY: str

    MODEL: str

    OLLAMA_HOST: str
    class Config:
        # Path to the .env file
        env_file = ".env.development"


# Create a single instance of the settings class
settings = Settings()
