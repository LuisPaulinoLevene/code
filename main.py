import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers.usuario import router as usuario_router
from routers.admin import router as admin_router
from routers.pages.unlock import router as pages_router
from routers import marca
from routers import modelo
from routers import config
from routers import calcular

# ==========================
# AMBIENTE
# ==========================
ENV = os.getenv(
    "ENV",
    "development"
)
# ==========================
# FASTAPI
# ==========================
app = FastAPI(
    title="API Usuários e Admins",
    docs_url=None if ENV == "production" else "/docs",
    redoc_url=None if ENV == "production" else "/redoc",
    openapi_url=None if ENV == "production" else "/openapi.json"
)
# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ==========================
# ROTAS
# ==========================
app.include_router(usuario_router)
app.include_router(admin_router)
app.include_router(pages_router)
app.include_router(calcular.router)
app.include_router(marca.router)
app.include_router(modelo.router)
app.include_router(config.router)

# ==========================
# CRIAR TABELAS
# ==========================
@app.on_event("startup")
def startup():
    Base.metadata.create_all(
        bind=engine
    )

# ==========================
# HOME
# ==========================
@app.get("/")
def home():
    return {
        "message": "API funcionando 🚀",
        "environment": ENV
    }