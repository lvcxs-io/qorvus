from math import ceil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.pagination import PaginationParams, PageResponse
from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/", response_model=PageResponse[UsuarioResponse])
def listar_usuarios(
    pagination: PaginationParams = Depends(), 
    db: Session = Depends(get_db)
):
    query = db.query(Usuario).filter(Usuario.status_removido == False)
    
    total = query.count()
    items = query.offset(pagination.skip).limit(pagination.size).all()
    total_pages = ceil(total / pagination.size) if total > 0 else 1
    
    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
        "total_pages": total_pages
    }

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Lógica de criação (com hash de senha)
    novo_usuario = Usuario(**usuario.model_dump())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.status_removido == False).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.status_removido == False).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    dados_atualizados = usuario_data.model_dump(exclude_unset=True)
    for key, value in dados_atualizados.items():
        setattr(usuario, key, value)
        
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.status_removido == False).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    usuario.status_removido = True
    db.commit()
    return None