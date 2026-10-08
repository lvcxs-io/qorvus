from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import Empresa, Usuario
from app.schemas.schemas import EmpresaResponse

router = APIRouter(prefix="/empresas", tags=["Empresas"])


@router.get("/minha", response_model=EmpresaResponse)
def get_my_company(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> Empresa:
    return db.query(Empresa).filter(Empresa.id == user.empresa_id).one()
