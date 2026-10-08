import re
from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    nome_completo: str = Field(min_length=2, max_length=100)
    cpf: str = Field(min_length=11, max_length=14)
    data_admissao: date
    email: EmailStr
    telefone: str = Field(min_length=8, max_length=20)
    senha: str = Field(min_length=8, max_length=128)

    @field_validator("cpf")
    @classmethod
    def normalize_cpf(cls, value: str) -> str:
        digits = re.sub(r"\D", "", value)
        if len(digits) != 11:
            raise ValueError("CPF deve conter 11 dígitos.")
        return digits

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class EmployeeUpdate(BaseModel):
    nome_completo: str | None = Field(None, min_length=2, max_length=100)
    cpf: str | None = Field(None, min_length=11, max_length=14)
    data_admissao: date | None = None
    email: EmailStr | None = None
    telefone: str | None = Field(None, min_length=8, max_length=20)
    status_ativo: bool | None = None

    @field_validator("cpf")
    @classmethod
    def normalize_cpf(cls, value: str | None) -> str | None:
        if value is None:
            return None
        digits = re.sub(r"\D", "", value)
        if len(digits) != 11:
            raise ValueError("CPF deve conter 11 dígitos.")
        return digits

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr | None) -> str | None:
        return str(value).strip().lower() if value is not None else None
