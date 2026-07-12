from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.modelo import Modelo
from models.marca import Marca

from schemas.modelo import (
    ModeloCreate,
    ModeloUpdate,
    ModeloResponse,
)


router = APIRouter(
    prefix="/modelos",
    tags=["Modelos"],
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# ==========================
# Criar Modelo
# ==========================

@router.post(
    "/",
    response_model=ModeloResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_modelo(
    dados: ModeloCreate,
    db: Session = Depends(get_db),
):

    # verificar se marca existe
    marca = db.get(
        Marca,
        dados.marca_id
    )


    if not marca:

        raise HTTPException(
            status_code=404,
            detail="Marca não encontrada."
        )



    # verificar modelo duplicado dentro da mesma marca

    existente = (
        db.query(Modelo)
        .filter(
            Modelo.modelo == dados.modelo,
            Modelo.marca_id == dados.marca_id
        )
        .first()
    )


    if existente:

        raise HTTPException(
            status_code=400,
            detail="Este modelo já existe nesta marca."
        )



    if dados.formula not in [1, 2, 3]:

        raise HTTPException(
            status_code=400,
            detail="A fórmula deve ser 1, 2 ou 3."
        )



    modelo = Modelo(
        modelo=dados.modelo,
        formula=dados.formula,
        marca_id=dados.marca_id
    )



    db.add(modelo)

    db.commit()

    db.refresh(modelo)


    return modelo





# ==========================
# Listar todos modelos
# ==========================

@router.get(
    "/",
    response_model=List[ModeloResponse],
)
def listar_modelos(
    db: Session = Depends(get_db),
):

    return (
        db.query(Modelo)
        .order_by(Modelo.modelo)
        .all()
    )





# ==========================
# Listar modelos por marca
# ==========================

@router.get(
    "/marca/{marca_id}",
    response_model=List[ModeloResponse],
)
def listar_modelos_por_marca(
    marca_id: int,
    db: Session = Depends(get_db),
):

    marca = db.get(
        Marca,
        marca_id
    )


    if not marca:

        raise HTTPException(
            status_code=404,
            detail="Marca não encontrada."
        )



    return (
        db.query(Modelo)
        .filter(
            Modelo.marca_id == marca_id
        )
        .order_by(Modelo.modelo)
        .all()
    )





# ==========================
# Buscar por ID
# ==========================

@router.get(
    "/{modelo_id}",
    response_model=ModeloResponse,
)
def obter_modelo(
    modelo_id: int,
    db: Session = Depends(get_db),
):

    modelo = db.get(
        Modelo,
        modelo_id
    )


    if not modelo:

        raise HTTPException(
            status_code=404,
            detail="Modelo não encontrado."
        )


    return modelo





# ==========================
# Atualizar
# ==========================

@router.put(
    "/{modelo_id}",
    response_model=ModeloResponse,
)
def atualizar_modelo(
    modelo_id: int,
    dados: ModeloUpdate,
    db: Session = Depends(get_db),
):

    modelo = db.get(
        Modelo,
        modelo_id
    )


    if not modelo:

        raise HTTPException(
            status_code=404,
            detail="Modelo não encontrado."
        )



    marca = db.get(
        Marca,
        dados.marca_id
    )


    if not marca:

        raise HTTPException(
            status_code=404,
            detail="Marca não encontrada."
        )



    if dados.formula not in [1, 2, 3]:

        raise HTTPException(
            status_code=400,
            detail="A fórmula deve ser 1, 2 ou 3."
        )



    duplicado = (
        db.query(Modelo)
        .filter(
            Modelo.modelo == dados.modelo,
            Modelo.marca_id == dados.marca_id,
            Modelo.id != modelo_id
        )
        .first()
    )



    if duplicado:

        raise HTTPException(
            status_code=400,
            detail="Já existe outro modelo com este nome nesta marca."
        )



    modelo.modelo = dados.modelo
    modelo.formula = dados.formula
    modelo.marca_id = dados.marca_id



    db.commit()

    db.refresh(modelo)


    return modelo





# ==========================
# Eliminar
# ==========================

@router.delete(
    "/{modelo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_modelo(
    modelo_id: int,
    db: Session = Depends(get_db),
):

    modelo = db.get(
        Modelo,
        modelo_id
    )


    if not modelo:

        raise HTTPException(
            status_code=404,
            detail="Modelo não encontrado."
        )



    db.delete(modelo)

    db.commit()



# ==========================
# Listar fórmulas disponíveis
# ==========================

@router.get("/formulas")
def listar_formulas():

    return [
        {
            "id": 1,
            "nome": "Fórmula 1",
            "funcao": "f1"
        },
        {
            "id": 2,
            "nome": "Fórmula 2",
            "funcao": "f2"
        },
        {
            "id": 3,
            "nome": "Fórmula 3",
            "funcao": "f3"
        }
    ]