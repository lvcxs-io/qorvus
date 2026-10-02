from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.models import Categoria
from app.schemas.schemas import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.core.database import get_db

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Categoria).offset(skip).limit(limit).all()

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = db.query(Categoria).filter(Categoria.nome == categoria.nome).first()
    if db_categoria:
        raise HTTPException(status_code=400, detail="Já existe uma categoria com este nome.")
    nova_categoria = Categoria(**categoria.model_dump())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(categoria_id: int, categoria_data: CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    dados_atualizados = categoria_data.model_dump(exclude_unset=True)
    for key, value in dados_atualizados.items():
        setattr(categoria, key, value)
    db.commit()
    db.refresh(categoria)
    return categoria