from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class MovementCreate(BaseModel):
    item_id: int
    tipo: Literal["ENTRADA", "SAIDA"]
    quantidade: int = Field(gt=0)


class MovementResponse(BaseModel):
    id: int
    item_id: int
    usuario_id: int
    tipo: Literal["ENTRADA", "SAIDA"]
    quantidade: int
    data_hora: datetime

    model_config = {"from_attributes": True}


class LowStockProduct(BaseModel):
    id: int
    nome: str
    quantidade: int
    limite_minimo: int


class RecentMovement(BaseModel):
    id: int
    produto: str
    tipo: Literal["ENTRADA", "SAIDA"]
    quantidade: int
    data_hora: datetime


class DailyMovementTotals(BaseModel):
    data: str
    entradas: int
    saidas: int


class DashboardSummaryResponse(BaseModel):
    total_produtos: int
    entradas_7_dias: int
    saidas_7_dias: int
    itens_estoque_baixo: int
    produtos_estoque_baixo: list[LowStockProduct]
    movimentacoes_recentes: list[RecentMovement]
    serie_movimentacoes: list[DailyMovementTotals]
