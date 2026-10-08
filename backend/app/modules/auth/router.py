from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import Usuario
from app.modules.auth.schemas import (
    AuthResponse,
    AuthUserResponse,
    CompanyOwnerRegistration,
    LoginRequest,
)
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_company_owner(
    registration: CompanyOwnerRegistration,
    db: Session = Depends(get_db),
) -> dict:
    return AuthService(db).register_company_owner(registration)


@router.post("/login", response_model=AuthResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)) -> dict:
    return AuthService(db).login(credentials)


@router.get("/me", response_model=AuthUserResponse)
def get_authenticated_user(user: Usuario = Depends(get_current_user)) -> Usuario:
    return user
