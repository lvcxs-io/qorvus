from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.models import Marca
from app.schemas.schemas import MarcaCreate, MarcaUpdate, MarcaResponse
from app.core.database import get_db

router = APIRouter(prefix="/marcas", tags=["Marcas"])

@router.get("/", response_model=List[MarcaResponse])
def listar_marcas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Marca).offset(skip).limit(limit).all()

@router.post("/", response_model=MarcaResponse, status_code=status.HTTP_201_CREATED)
def criar_marca(marca: MarcaCreate, db: Session = Depends(get_db)):
    db_marca = db.query(Marca).filter(Marca.nome == marca.nome).first()
    if db_marca:
        raise HTTPException(status_code=400, detail="Já existe uma marca com este nome.")
    nova_marca = Marca(**marca.model_dump())
    db.add(nova_marca)
    db.commit()
    db.refresh(nova_marca)
    return nova_marca

@router.get("/{marca_id}", response_model=MarcaResponse)
def obter_marca(marca_id: int, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada.")
    return marca

@router.put("/{marca_id}", response_model=MarcaResponse)
def atualizar_marca(marca_id: int, marca_data: MarcaUpdate, db: Session = Depends(get_db)):
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada.")
    dados_atualizados = marca_data.model_dump(exclude_unset=True)
    for key, value in dados_atualizados.items():
        setattr(marca, key, value)
    db.commit()
    db.refresh(marca)
    return marca