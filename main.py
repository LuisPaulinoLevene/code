import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from decouple import config

from database import engine, Base

from routers.usuario import router as usuario_router
from routers.admin import router as admin_router
from routers.pages.unlock import router as pages_router
from routers.pages import x

from routers import marca
from routers import modelo
from routers import config as config_router
from routers import calcular
from routers import saldo

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
# SESSION ADMIN
# ==========================
SECRET_KEY = config(
    "SECRET_KEY"
)
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="admin_session",
    https_only=ENV == "production",
    same_site="lax"
)

# ==========================
# CORS
# ==========================
if ENV == "production":
    origins = [
        "https://code-unlock.onrender.com/"
    ]
else:
    origins = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=["*"]
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
app.include_router(config_router.router)
app.include_router(saldo.router)
app.include_router(x.router)

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
        "message":
        "API funcionando 🚀",

        "environment":
        ENV

    }