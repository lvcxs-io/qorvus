from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.models import Empresa
from app.schemas.schemas import EmpresaCreate, EmpresaResponse
from app.core.database import get_db

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.get("/", response_model=List[EmpresaResponse])
def listar_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Empresa).offset(skip).limit(limit).all()

@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
    if db_empresa:
        raise HTTPException(status_code=400, detail="Já existe uma empresa registada com este CNPJ.")
    
    nova_empresa = Empresa(**empresa.model_dump())
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa