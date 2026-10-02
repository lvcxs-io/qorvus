from fastapi import Query
from pydantic import BaseModel
from typing import Generic, TypeVar, List
from math import ceil

# Parâmetros de entrada validados automaticamente
class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Número da página"),
        size: int = Query(10, ge=1, le=100, description="Itens por página")
    ):
        self.page = page
        self.size = size
        self.skip = (page - 1) * size

# Estrutura de resposta padrão Angular
T = TypeVar("T")

class PageResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    total_pages: int
    

