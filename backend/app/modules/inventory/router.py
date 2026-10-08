from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_company_admin
from app.core.pagination import PageResponse, PaginationParams
from app.models import Usuario
from app.modules.inventory.schemas import (
    DashboardSummaryResponse,
    MovementCreate,
    MovementResponse,
)
from app.modules.inventory.service import InventoryService
from app.schemas.schemas import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
    ItemCreate,
    ItemResponse,
    ItemUpdate,
    MarcaCreate,
    MarcaResponse,
    MarcaUpdate,
)

router = APIRouter()


def _service(db: Session, user: Usuario) -> InventoryService:
    return InventoryService(db, user)


@router.get("/categorias", response_model=list[CategoriaResponse], tags=["Categorias"])
def list_categories(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> list:
    return _service(db, user).list_categories()


@router.post(
    "/categorias",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Categorias"],
)
def create_category(
    data: CategoriaCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> object:
    return _service(db, user).create_category(data)


@router.get(
    "/categorias/{category_id}",
    response_model=CategoriaResponse,
    tags=["Categorias"],
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> object:
    return _service(db, user).get_category(category_id)


@router.put("/categorias/{category_id}", response_model=CategoriaResponse, tags=["Categorias"])
def update_category(
    category_id: int,
    data: CategoriaUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> object:
    return _service(db, user).update_category(category_id, data)


@router.get("/marcas", response_model=list[MarcaResponse], tags=["Marcas"])
def list_brands(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> list:
    return _service(db, user).list_brands()


@router.post(
    "/marcas",
    response_model=MarcaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Marcas"],
)
def create_brand(
    data: MarcaCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> object:
    return _service(db, user).create_brand(data)


@router.get("/marcas/{brand_id}", response_model=MarcaResponse, tags=["Marcas"])
def get_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> object:
    return _service(db, user).get_brand(brand_id)


@router.put("/marcas/{brand_id}", response_model=MarcaResponse, tags=["Marcas"])
def update_brand(
    brand_id: int,
    data: MarcaUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> object:
    return _service(db, user).update_brand(brand_id, data)


@router.get(
    "/itens",
    response_model=PageResponse[ItemResponse],
    tags=["Itens"],
)
def list_items(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> dict:
    return _service(db, user).list_items(pagination)


@router.post(
    "/itens",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Itens"],
)
def create_item(
    data: ItemCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> object:
    return _service(db, user).create_item(data)


@router.get("/itens/{item_id}", response_model=ItemResponse, tags=["Itens"])
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> object:
    return _service(db, user).get_item(item_id)


@router.put("/itens/{item_id}", response_model=ItemResponse, tags=["Itens"])
def update_item(
    item_id: int,
    data: ItemUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> object:
    return _service(db, user).update_item(item_id, data)


@router.delete(
    "/itens/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Itens"],
)
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_company_admin),
) -> None:
    _service(db, user).remove_item(item_id)


@router.get(
    "/movimentacoes",
    response_model=PageResponse[MovementResponse],
    tags=["Movimentações"],
)
def list_movements(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> dict:
    return _service(db, user).list_movements(pagination)


@router.post(
    "/movimentacoes",
    response_model=MovementResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Movimentações"],
)
def create_movement(
    data: MovementCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> object:
    return _service(db, user).create_movement(data)


@router.get(
    "/movimentacoes/{movement_id}",
    response_model=MovementResponse,
    tags=["Movimentações"],
)
def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> object:
    return _service(db, user).get_movement(movement_id)


@router.get(
    "/dashboard/resumo",
    response_model=DashboardSummaryResponse,
    tags=["Dashboard"],
)
def dashboard_summary(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
) -> dict:
    return _service(db, user).dashboard_summary()
