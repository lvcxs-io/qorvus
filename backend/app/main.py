from fastapi import FastAPI
from app.routers import categoria, marca, item, movimentacao, empresa, usuario

app = FastAPI(
    title="Qorvus - Bella Vitta API",
    version="1.0.0",
    description="API para gestão de estoque"
)

# Registar todos os routers
app.include_router(empresa.router)
app.include_router(usuario.router)
app.include_router(categoria.router)
app.include_router(marca.router)
app.include_router(item.router)
app.include_router(movimentacao.router)

@app.get("/")
def root():
    return {"mensagem": "Criado com sucesso!", "status": "online"}