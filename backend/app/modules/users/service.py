from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.core.security import hash_password
from app.models import Usuario
from app.modules.users.schemas import EmployeeCreate, EmployeeUpdate
from app.schemas.schemas import UsuarioResponse
from math import ceil


class UserService:
    def __init__(self, db: Session, company_id: int, requester_id: int) -> None:
        self._db = db
        self._company_id = company_id
        self._requester_id = requester_id

    def list_employees(self, pagination: PaginationParams) -> dict:
        query = self._db.query(Usuario).filter(Usuario.empresa_id == self._company_id)
        total = query.count()
        users = (
            query.order_by(Usuario.nome_completo)
            .offset(pagination.skip)
            .limit(pagination.size)
            .all()
        )
        return {
            "items": users,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "total_pages": ceil(total / pagination.size) if total else 1,
        }

    def create_employee(self, data: EmployeeCreate) -> Usuario:
        employee = Usuario(
            nome_completo=data.nome_completo.strip(),
            cpf=data.cpf,
            cargo="FUNCIONARIO",
            data_admissao=data.data_admissao,
            empresa_id=self._company_id,
            email=str(data.email),
            telefone=data.telefone.strip(),
            senha_hash=hash_password(data.senha),
            perfil="FUNCIONARIO",
            status_ativo=True,
        )
        return self._save(employee)

    def update_employee(self, user_id: int, data: EmployeeUpdate) -> Usuario:
        if user_id == self._requester_id and data.status_ativo is False:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Não é possível desativar a própria conta.",
            )
        employee = self._get_employee(user_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)
        return self._save(employee)

    def deactivate_employee(self, user_id: int, requester_id: int) -> None:
        if user_id == requester_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Não é possível desativar a própria conta.",
            )
        employee = self._get_employee(user_id)
        employee.status_ativo = False
        self._save(employee)

    def _get_employee(self, user_id: int) -> Usuario:
        employee = (
            self._db.query(Usuario)
            .filter(
                Usuario.id == user_id,
                Usuario.empresa_id == self._company_id,
                Usuario.perfil == "FUNCIONARIO",
            )
            .first()
        )
        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado.",
            )
        return employee

    def _save(self, employee: Usuario) -> Usuario:
        try:
            self._db.add(employee)
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CPF ou e-mail já está cadastrado.",
            ) from None
        self._db.refresh(employee)
        return employee
