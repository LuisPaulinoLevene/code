from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.usuario import Usuario
from models.saldo import Saldo
from schemas.saldo import (
    SaldoCreate,
    SaldoUpdate,
    SaldoResponse,
)

router = APIRouter(
    prefix="/saldos",
    tags=["Saldos"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Listar utilizadores
@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


# Criar saldo para um utilizador
@router.post("/", response_model=SaldoResponse)
def criar_saldo(
    dados: SaldoCreate,
    db: Session = Depends(get_db),
):
    usuario = db.get(Usuario, dados.usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    existe = (
        db.query(Saldo)
        .filter(Saldo.usuario_id == dados.usuario_id)
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Este usuário já possui saldo."
        )

    saldo = Saldo(
        usuario_id=dados.usuario_id,
        saldo=dados.saldo,
    )

    db.add(saldo)
    db.commit()
    db.refresh(saldo)

    return saldo


# Listar saldos
@router.get("/", response_model=List[SaldoResponse])
def listar_saldos(db: Session = Depends(get_db)):
    return db.query(Saldo).all()


# Consultar saldo por usuário
@router.get("/{usuario_id}", response_model=SaldoResponse)
def obter_saldo(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    saldo = (
        db.query(Saldo)
        .filter(Saldo.usuario_id == usuario_id)
        .first()
    )

    if not saldo:
        raise HTTPException(
            status_code=404,
            detail="Saldo não encontrado."
        )

    return saldo


# Atualizar saldo
@router.put("/{usuario_id}", response_model=SaldoResponse)
def atualizar_saldo(
    usuario_id: int,
    dados: SaldoUpdate,
    db: Session = Depends(get_db),
):
    saldo = (
        db.query(Saldo)
        .filter(Saldo.usuario_id == usuario_id)
        .first()
    )

    if not saldo:
        raise HTTPException(
            status_code=404,
            detail="Saldo não encontrado."
        )

    saldo.saldo = dados.saldo

    db.commit()
    db.refresh(saldo)

    return saldo


# Remover saldo
@router.delete("/{usuario_id}")
def remover_saldo(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    saldo = (
        db.query(Saldo)
        .filter(Saldo.usuario_id == usuario_id)
        .first()
    )

    if not saldo:
        raise HTTPException(
            status_code=404,
            detail="Saldo não encontrado."
        )

    db.delete(saldo)
    db.commit()

    return {
        "message": "Saldo removido com sucesso."
    }