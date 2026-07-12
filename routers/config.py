from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.config import Config
from schemas.config import (
    ConfigCreate,
    ConfigUpdate,
    ConfigResponse,
)

router = APIRouter(
    prefix="/config",
    tags=["Configuração"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ConfigResponse)
def criar_config(
    dados: ConfigCreate,
    db: Session = Depends(get_db),
):
    existe = db.query(Config).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="A configuração já existe."
        )

    config = Config(
        preco_codigo=dados.preco_codigo
    )

    db.add(config)
    db.commit()
    db.refresh(config)

    return config


@router.get("/", response_model=ConfigResponse)
def obter_config(
    db: Session = Depends(get_db),
):
    config = db.query(Config).first()

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuração não encontrada."
        )

    return config


@router.put("/", response_model=ConfigResponse)
def atualizar_config(
    dados: ConfigUpdate,
    db: Session = Depends(get_db),
):
    config = db.query(Config).first()

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuração não encontrada."
        )

    config.preco_codigo = dados.preco_codigo

    db.commit()
    db.refresh(config)

    return config


@router.delete("/")
def remover_config(
    db: Session = Depends(get_db),
):
    config = db.query(Config).first()

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuração não encontrada."
        )

    db.delete(config)
    db.commit()

    return {
        "message": "Configuração removida com sucesso."
    }