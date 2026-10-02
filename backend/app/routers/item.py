from math import ceil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PageResponse
from app.models.models import Item
from app.schemas.schemas import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/itens", tags=["Itens"])

@router.get("/", response_model=PageResponse[ItemResponse])
def listar_itens(
    pagination: PaginationParams = Depends(), 
    db: Session = Depends(get_db)
):
    query = db.query(Item).filter(Item.status_removido == False)
    
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

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def criar_item(item: ItemCreate, db: Session = Depends(get_db)):
    novo_item = Item(**item.model_dump())
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return novo_item

@router.get("/{item_id}", response_model=ItemResponse)
def obter_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.status_removido == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
def atualizar_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.status_removido == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    dados_atualizados = item_data.model_dump(exclude_unset=True)
    for key, value in dados_atualizados.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.status_removido == False).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado.")
    item.status_removido = True
    db.commit()
    return None