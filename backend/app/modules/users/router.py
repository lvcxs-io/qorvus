from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_company_admin
from app.core.pagination import PageResponse, PaginationParams
from app.models import Usuario
from app.modules.users.schemas import EmployeeCreate, EmployeeUpdate
from app.modules.users.service import UserService
from app.schemas.schemas import UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/", response_model=PageResponse[UsuarioResponse])
def list_employees(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> dict:
    return UserService(db, user.empresa_id, user.id).list_employees(pagination)


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> Usuario:
    return UserService(db, user.empresa_id, user.id).create_employee(data)


@router.put("/{user_id}", response_model=UsuarioResponse)
def update_employee(
    user_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> Usuario:
    return UserService(db, user.empresa_id, user.id).update_employee(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_employee(
    user_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> None:
    UserService(db, user.empresa_id, user.id).deactivate_employee(user_id, user.id)
