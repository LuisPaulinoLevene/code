from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models.marca import Marca
from schemas.marca import (
    MarcaCreate,
    MarcaUpdate,
    MarcaResponse,
)

router = APIRouter(
    prefix="/marcas",
    tags=["Marcas"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=MarcaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_marca(
    dados: MarcaCreate,
    db: Session = Depends(get_db),
):
    existe = (
        db.query(Marca)
        .filter(Marca.marca == dados.marca)
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Marca já existe."
        )

    marca = Marca(**dados.model_dump())

    db.add(marca)
    db.commit()
    db.refresh(marca)

    return marca


@router.get(
    "/",
    response_model=List[MarcaResponse],
)
def listar_marcas(
    db: Session = Depends(get_db),
):
    return db.query(Marca).order_by(Marca.marca).all()


@router.get(
    "/{marca_id}",
    response_model=MarcaResponse,
)
def obter_marca(
    marca_id: int,
    db: Session = Depends(get_db),
):
    marca = db.get(Marca, marca_id)

    if not marca:
        raise HTTPException(
            status_code=404,
            detail="Marca não encontrada."
        )

    return marca


@router.put(
    "/{marca_id}",
    response_model=MarcaResponse,
)
def atualizar_marca(
    marca_id: int,
    dados: MarcaUpdate,
    db: Session = Depends(get_db),
):
    marca = db.get(Marca, marca_id)

    if not marca:
        raise HTTPException(
            status_code=404,
            detail="Marca não encontrada."
        )

    marca.marca = dados.marca

    db.commit()
    db.refresh(marca)

    return marca


@router.delete(
    "/{marca_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_marca(
    marca_id: int,
    db: Session = Depends(get_db),
):
    marca = db.get(Marca, marca_id)

    if not marca:
        raise HTTPException(
            status_code=404,
            detail="Marca não encontrada."
        )

    db.delete(marca)
    db.commit()