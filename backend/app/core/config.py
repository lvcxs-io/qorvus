from pathlib import Path
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Localiza o diretório raiz do backend independente de onde o terminal for executado
# app/core/config.py -> parent(core) -> parent(app) -> parent(backend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "QORVUS API"
    DATABASE_URL: str
    JWT_SECRET_KEY: SecretStr
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, gt=0, le=1440)
    FRONTEND_ORIGINS: list[str] = ["http://localhost:4200", "http://127.0.0.1:4200"]

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validate_jwt_secret(cls, secret: SecretStr) -> SecretStr:
        if len(secret.get_secret_value()) < 32:
            raise ValueError("JWT_SECRET_KEY precisa ter pelo menos 32 caracteres.")
        return secret

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# -----------------------------------------------------------------------------------------
# RESUMO PARA ENTENDERMOS:
# -----------------------------------------------------------------------------------------
# 1 - 'PROJECT_NAME' e 'DATABASE_URL' definem as variáveis de ambiente necessárias.
# 2 - 'BASE_DIR' garante que o Pydantic encontre o arquivo '.env' na raiz do projeto,
#     mesmo se você rodar o 'uvicorn' de fora da pasta do backend.
# 3 - 'SettingsConfigDict' é a sintaxe atual e recomendada do Pydantic v2 / pydantic-settings.