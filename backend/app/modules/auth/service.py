from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models import Empresa, Usuario
from app.modules.auth.schemas import CompanyOwnerRegistration, LoginRequest


class AuthService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def register_company_owner(self, registration: CompanyOwnerRegistration) -> dict:
        company = Empresa(
            nome_empresa=registration.nome_empresa.strip(),
            cnpj=registration.cnpj,
        )
        user = Usuario(
            nome_completo=registration.nome_completo.strip(),
            cpf=registration.cpf,
            cargo="ADMINISTRADOR",
            data_admissao=date.today(),
            email=str(registration.email),
            telefone=registration.telefone.strip(),
            senha_hash=hash_password(registration.senha),
            perfil="ADMINISTRADOR",
            status_ativo=True,
        )

        try:
            with self._db.begin():
                self._db.add(company)
                self._db.flush()
                user.empresa_id = company.id
                self._db.add(user)
                self._db.flush()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CNPJ, CPF ou e-mail já está cadastrado.",
            ) from None

        self._db.refresh(user)
        return self._auth_response(user)

    def login(self, credentials: LoginRequest) -> dict:
        user = (
            self._db.query(Usuario)
            .filter(
                Usuario.email == str(credentials.email),
                Usuario.status_ativo.is_(True),
            )
            .first()
        )
        if user is None or not verify_password(credentials.senha, user.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return self._auth_response(user)

    @staticmethod
    def _auth_response(user: Usuario) -> dict:
        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer",
            "user": user,
        }
