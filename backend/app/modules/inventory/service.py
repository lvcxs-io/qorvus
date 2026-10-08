from datetime import date, datetime, time, timedelta
from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams
from app.models import Categoria, Item, Marca, Movimentacao, Usuario
from app.schemas.schemas import (
    CategoriaCreate,
    CategoriaUpdate,
    ItemCreate,
    ItemUpdate,
    MarcaCreate,
    MarcaUpdate,
)
from app.modules.inventory.schemas import MovementCreate


class InventoryService:
    def __init__(self, db: Session, user: Usuario) -> None:
        self._db = db
        self._user = user
        self._company_id = user.empresa_id

    def list_categories(self) -> list[Categoria]:
        return (
            self._db.query(Categoria)
            .filter(Categoria.empresa_id == self._company_id)
            .order_by(Categoria.nome)
            .all()
        )

    def get_category(self, category_id: int) -> Categoria:
        return self._get_company_record(Categoria, category_id, "Categoria")

    def create_category(self, data: CategoriaCreate) -> Categoria:
        category = Categoria(empresa_id=self._company_id, **data.model_dump())
        return self._save(category)

    def update_category(self, category_id: int, data: CategoriaUpdate) -> Categoria:
        category = self._get_company_record(Categoria, category_id, "Categoria")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        return self._save(category)

    def list_brands(self) -> list[Marca]:
        return (
            self._db.query(Marca)
            .filter(Marca.empresa_id == self._company_id)
            .order_by(Marca.nome)
            .all()
        )

    def get_brand(self, brand_id: int) -> Marca:
        return self._get_company_record(Marca, brand_id, "Marca")

    def create_brand(self, data: MarcaCreate) -> Marca:
        brand = Marca(empresa_id=self._company_id, **data.model_dump())
        return self._save(brand)

    def update_brand(self, brand_id: int, data: MarcaUpdate) -> Marca:
        brand = self._get_company_record(Marca, brand_id, "Marca")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(brand, field, value)
        return self._save(brand)

    def list_items(self, pagination: PaginationParams) -> dict:
        query = self._db.query(Item).filter(
            Item.empresa_id == self._company_id,
            Item.status_removido.is_(False),
        )
        return self._page(query, pagination)

    def get_item(self, item_id: int) -> Item:
        return self._get_company_record(Item, item_id, "Produto", active_only=True)

    def create_item(self, data: ItemCreate) -> Item:
        values = data.model_dump()
        if values.get("quantidade", 0) != 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O saldo inicial deve ser registrado como uma movimentação de entrada.",
            )
        self._get_company_record(Categoria, values["categoria_id"], "Categoria")
        if values.get("marca_id") is not None:
            self._get_company_record(Marca, values["marca_id"], "Marca")
        values["quantidade"] = 0
        return self._save(Item(empresa_id=self._company_id, **values))

    def update_item(self, item_id: int, data: ItemUpdate) -> Item:
        item = self.get_item(item_id)
        values = data.model_dump(exclude_unset=True)
        if "quantidade" in values or "status_removido" in values:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Estoque só pode ser alterado por movimentações.",
            )
        if "categoria_id" in values:
            self._get_company_record(Categoria, values["categoria_id"], "Categoria")
        if values.get("marca_id") is not None:
            self._get_company_record(Marca, values["marca_id"], "Marca")
        for field, value in values.items():
            setattr(item, field, value)
        return self._save(item)

    def remove_item(self, item_id: int) -> None:
        item = self.get_item(item_id)
        item.status_removido = True
        self._save(item)

    def list_movements(self, pagination: PaginationParams) -> dict:
        query = self._db.query(Movimentacao).filter(
            Movimentacao.empresa_id == self._company_id
        )
        return self._page(query, pagination, order_by=Movimentacao.data_hora.desc())

    def get_movement(self, movement_id: int) -> Movimentacao:
        return self._get_company_record(Movimentacao, movement_id, "Movimentação")

    def create_movement(self, data: MovementCreate) -> Movimentacao:
        item = (
            self._db.query(Item)
            .filter(
                Item.id == data.item_id,
                Item.empresa_id == self._company_id,
                Item.status_removido.is_(False),
            )
            .with_for_update()
            .first()
        )
        if item is None:
            raise self._not_found("Produto")
        if data.tipo == "SAIDA" and item.quantidade < data.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Estoque insuficiente. Saldo atual: {item.quantidade}.",
            )

        if data.tipo == "ENTRADA":
            item.quantidade += data.quantidade
        else:
            item.quantidade -= data.quantidade

        movement = Movimentacao(
            empresa_id=self._company_id,
            usuario_id=self._user.id,
            item_id=item.id,
            tipo=data.tipo,
            quantidade=data.quantidade,
        )
        self._db.add(movement)
        return self._save(movement)

    def dashboard_summary(self) -> dict:
        today = date.today()
        start_date = datetime.combine(today - timedelta(days=6), time.min)
        movement_rows = (
            self._db.query(
                func.date(Movimentacao.data_hora),
                Movimentacao.tipo,
                func.coalesce(func.sum(Movimentacao.quantidade), 0),
            )
            .filter(
                Movimentacao.empresa_id == self._company_id,
                Movimentacao.data_hora >= start_date,
            )
            .group_by(func.date(Movimentacao.data_hora), Movimentacao.tipo)
            .all()
        )
        daily: dict[str, dict[str, int]] = {}
        for movement_date, movement_type, quantity in movement_rows:
            key = str(movement_date)
            daily.setdefault(key, {"entradas": 0, "saidas": 0})
            daily[key]["entradas" if movement_type == "ENTRADA" else "saidas"] = int(
                quantity
            )

        low_stock_query = self._db.query(Item).filter(
            Item.empresa_id == self._company_id,
            Item.status_removido.is_(False),
            Item.quantidade <= Item.limite_minimo,
        )
        low_stock_count = low_stock_query.count()
        low_stock = (
            low_stock_query
            .order_by(Item.quantidade.asc(), Item.nome)
            .limit(10)
            .all()
        )
        recent_movements = (
            self._db.query(Movimentacao, Item.nome)
            .join(Item, Item.id == Movimentacao.item_id)
            .filter(Movimentacao.empresa_id == self._company_id)
            .order_by(Movimentacao.data_hora.desc())
            .limit(5)
            .all()
        )
        total_products = (
            self._db.query(func.count(Item.id))
            .filter(Item.empresa_id == self._company_id, Item.status_removido.is_(False))
            .scalar()
        )
        movement_series = []
        for offset in range(6, -1, -1):
            movement_date = today - timedelta(days=offset)
            totals = daily.get(
                movement_date.isoformat(),
                {"entradas": 0, "saidas": 0},
            )
            movement_series.append({"data": movement_date.isoformat(), **totals})

        return {
            "total_produtos": int(total_products or 0),
            "entradas_7_dias": sum(day["entradas"] for day in daily.values()),
            "saidas_7_dias": sum(day["saidas"] for day in daily.values()),
            "itens_estoque_baixo": low_stock_count,
            "produtos_estoque_baixo": [
                {
                    "id": item.id,
                    "nome": item.nome,
                    "quantidade": item.quantidade,
                    "limite_minimo": item.limite_minimo,
                }
                for item in low_stock
            ],
            "movimentacoes_recentes": [
                {
                    "id": movement.id,
                    "produto": product_name,
                    "tipo": movement.tipo,
                    "quantidade": movement.quantidade,
                    "data_hora": movement.data_hora,
                }
                for movement, product_name in recent_movements
            ],
            "serie_movimentacoes": movement_series,
        }

    def _get_company_record(
        self,
        model: type,
        record_id: int,
        label: str,
        *,
        active_only: bool = False,
    ):
        query = self._db.query(model).filter(
            model.id == record_id,
            model.empresa_id == self._company_id,
        )
        if active_only and model is Item:
            query = query.filter(Item.status_removido.is_(False))
        record = query.first()
        if record is None:
            raise self._not_found(label)
        return record

    @staticmethod
    def _not_found(label: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{label} não encontrado.",
        )

    def _save(self, record):
        try:
            self._db.add(record)
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Registro duplicado ou relacionado a dados inválidos desta empresa.",
            ) from None
        self._db.refresh(record)
        return record

    def _page(self, query, pagination: PaginationParams, order_by=None) -> dict:
        total = query.count()
        if order_by is not None:
            query = query.order_by(order_by)
        items = query.offset(pagination.skip).limit(pagination.size).all()
        return {
            "items": items,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "total_pages": ceil(total / pagination.size) if total else 1,
        }
