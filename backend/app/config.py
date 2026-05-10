import os
from pathlib import Path
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# "dev" / "prod" en el env para detectar que config usar
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev").lower()

BASE_DIR = Path(__file__).parent.parent

if ENVIRONMENT == "prod":
    ENV_FILE = BASE_DIR / ".env.prod"
else:
    ENV_FILE = BASE_DIR / ".env.dev"

if not ENV_FILE.exists():
    ENV_FILE = BASE_DIR / ".env"


class Config(BaseSettings):
    ENVIRONMENT: str = "dev"

    # DB
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    # BACK
    PORT: int = 8080

    # JWT
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60)

    # SUBIDAS
    UPLOAD_DIR: str = "/tmp/uploads"
    TAMAÑO_LIMITE: int = 1000 * 1024 * 1024  # 1GB

    # PAPELERA
    DIAS_PAPELERA: int = 30

    # POOL
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600  # 1 H

    # CORS
    ALLOWED_ORIGINS: list[str] = Field(default=["http://localhost:5173"])

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False
    )


config = Config()
