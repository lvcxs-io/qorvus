from math import ceil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PageResponse
from app.models.models import Movimentacao, Item
from app.schemas.schemas import MovimentacaoCreate, MovimentacaoResponse

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])

@router.get("/", response_model=PageResponse[MovimentacaoResponse])
def listar_movimentacoes(
    pagination: PaginationParams = Depends(), 
    db: Session = Depends(get_db)
):
    query = db.query(Movimentacao)
    
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

@router.post("/", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimentacao(movimentacao: MovimentacaoCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == movimentacao.item_id, Item.status_removido == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado ou inativo.")
    
    # Validação de estoque para saídas
    if movimentacao.tipo == "SAIDA" and item.quantidade < movimentacao.quantidade:
        raise HTTPException(
            status_code=400, 
            detail=f"Estoque insuficiente. Saldo atual: {item.quantidade}"
        )
    
    # Atualiza a quantidade em estoque do item
    if movimentacao.tipo == "ENTRADA":
        item.quantidade += movimentacao.quantidade
    elif movimentacao.tipo == "SAIDA":
        item.quantidade -= movimentacao.quantidade

    nova_movimentacao = Movimentacao(**movimentacao.model_dump())
    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)
    return nova_movimentacao

@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
def obter_movimentacao(movimentacao_id: int, db: Session = Depends(get_db)):
    movimentacao = db.query(Movimentacao).filter(Movimentacao.id == movimentacao_id).first()
    if not movimentacao:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada.")
    return movimentacao