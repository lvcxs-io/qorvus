from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.companies.router import router as companies_router
from app.modules.inventory.router import router as inventory_router
from app.modules.users.router import router as users_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    description="API multiempresa para gestão de estoque.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(companies_router)
app.include_router(users_router)
app.include_router(inventory_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"mensagem": "Qorvus API online.", "status": "online"}
