import re

from pydantic import BaseModel, EmailStr, Field, field_validator


def _digits_only(value: str) -> str:
    return re.sub(r"\D", "", value)


class CompanyOwnerRegistration(BaseModel):
    nome_empresa: str = Field(min_length=2, max_length=150)
    cnpj: str = Field(min_length=14, max_length=18)
    nome_completo: str = Field(min_length=2, max_length=100)
    cpf: str = Field(min_length=11, max_length=14)
    email: EmailStr = Field(max_length=70)
    telefone: str = Field(min_length=8, max_length=20)
    senha: str = Field(min_length=8, max_length=128)

    @field_validator("cnpj")
    @classmethod
    def normalize_cnpj(cls, value: str) -> str:
        digits = _digits_only(value)
        if len(digits) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos.")
        return digits

    @field_validator("cpf")
    @classmethod
    def normalize_cpf(cls, value: str) -> str:
        digits = _digits_only(value)
        if len(digits) != 11:
            raise ValueError("CPF deve conter 11 dígitos.")
        return digits

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class LoginRequest(BaseModel):
    email: EmailStr = Field(max_length=70)
    senha: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class AuthUserResponse(BaseModel):
    id: int
    nome_completo: str
    email: EmailStr
    empresa_id: int
    perfil: str

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUserResponse
