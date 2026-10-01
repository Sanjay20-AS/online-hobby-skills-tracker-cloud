from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./hobbytracker.db"
    jwt_secret: str = "change-this-secret"
    jwt_expire_minutes: int = 1440
    cors_origins: str = "http://localhost:5173"
    max_upload_mb: int = 5
    s3_endpoint_url: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    s3_bucket: str = "hobby-tracker"
    s3_region: str = "us-east-1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
