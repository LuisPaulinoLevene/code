from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from database import SessionLocal

from models.marca import Marca
from models.modelo import Modelo
from models.usuario import Usuario
from models.saldo import Saldo
from models.config import Config

from schemas.calcular import (
    CalcularCreate,
    CalcularResponse,
    RecargaCreate,
)

# IMPORTAR FORMULAS REAIS
from utils.formulas import f1, f2, f3


router = APIRouter(
    prefix="/calcular",
    tags=["Calcular Código"]
)



# =================================================
# CONEXÃO BANCO
# =================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# =================================================
# FUNÇÕES DE CÁLCULO
# =================================================

def calcular_formula(
    imei: str,
    formula: int
):

    if formula == 1:

        return f1(imei)


    elif formula == 2:

        return f2(imei)


    elif formula == 3:

        return f3(imei)


    else:

        raise HTTPException(
            status_code=400,
            detail="Fórmula inválida."
        )



# =================================================
# LISTAR MARCAS
# =================================================

@router.get("/marcas")
def listar_marcas(
    db: Session = Depends(get_db)
):

    return (
        db.query(Marca)
        .order_by(Marca.marca)
        .all()
    )



# =================================================
# LISTAR MODELOS POR MARCA
# =================================================

@router.get("/modelos/{marca_id}")
def listar_modelos(
    marca_id: int,
    db: Session = Depends(get_db)
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



# =================================================
# CONSULTAR SALDO
# =================================================

@router.get("/saldo/{usuario_id}")
def consultar_saldo(
    usuario_id: int,
    db: Session = Depends(get_db)
):

    usuario = db.get(
        Usuario,
        usuario_id
    )


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )


    saldo = (
        db.query(Saldo)
        .filter(
            Saldo.usuario_id == usuario_id
        )
        .first()
    )


    if not saldo:

        return {
            "usuario_id": usuario_id,
            "saldo": 0
        }


    return {
        "usuario_id": usuario_id,
        "saldo": saldo.saldo
    }



# =================================================
# CALCULAR CÓDIGO
# =================================================

@router.post(
    "/",
    response_model=CalcularResponse
)
def calcular_codigo(
    dados: CalcularCreate,
    db: Session = Depends(get_db)
):


    # validar IMEI

    if not dados.imei.isdigit():

        raise HTTPException(
            status_code=400,
            detail="IMEI deve conter somente números."
        )


    if len(dados.imei) != 15:

        raise HTTPException(
            status_code=400,
            detail="IMEI deve ter exatamente 15 dígitos."
        )



    # verificar usuário

    usuario = db.get(
        Usuario,
        dados.usuario_id
    )


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )



    # verificar marca

    marca = db.get(
        Marca,
        dados.marca_id
    )


    if not marca:

        raise HTTPException(
            status_code=404,
            detail="Marca não encontrada."
        )



    # verificar modelo

    modelo = db.get(
        Modelo,
        dados.modelo_id
    )


    if not modelo:

        raise HTTPException(
            status_code=404,
            detail="Modelo não encontrado."
        )



    # garantir modelo pertence à marca

    if modelo.marca_id != dados.marca_id:

        raise HTTPException(
            status_code=400,
            detail="Este modelo não pertence a esta marca."
        )



    # buscar saldo

    saldo = (
        db.query(Saldo)
        .filter(
            Saldo.usuario_id == dados.usuario_id
        )
        .first()
    )


    if not saldo:

        raise HTTPException(
            status_code=400,
            detail="Usuário sem saldo. Faça uma recarga."
        )



    # buscar preço

    config = (
        db.query(Config)
        .first()
    )


    if not config:

        raise HTTPException(
            status_code=500,
            detail="Preço do código não configurado."
        )



    # verificar saldo

    if saldo.saldo < config.preco_codigo:

        raise HTTPException(
            status_code=400,
            detail={
                "mensagem": "Saldo insuficiente.",
                "saldo_atual": saldo.saldo,
                "preco_codigo": config.preco_codigo
            }
        )



    # =========================================
    # GERAR CÓDIGO USANDO FORMULA REAL
    # =========================================

    codigo = calcular_formula(
        dados.imei,
        modelo.formula
    )



    # descontar saldo

    saldo.saldo -= config.preco_codigo


    db.commit()

    db.refresh(saldo)



    return {

        "imei": dados.imei,

        "marca_id": dados.marca_id,

        "modelo_id": dados.modelo_id,

        "codigo": codigo,

        "saldo_restante": saldo.saldo

    }




# =================================================
# RECARGA MPESA / EMOLA
# =================================================

@router.post("/recarga")
def recarregar_saldo(
    dados: RecargaCreate,
    db: Session = Depends(get_db)
):


    usuario = db.get(
        Usuario,
        dados.usuario_id
    )


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )



    if dados.metodo.lower() == "emola":

        url = (
            "https://mozpayment.co.mz/api/1.1/"
            "wf/pagamentorotativoemola"
        )


    elif dados.metodo.lower() == "mpesa":

        url = (
            "https://mozpayment.co.mz/api/1.1/"
            "wf/pagamentorotativompesa"
        )


    else:

        raise HTTPException(
            status_code=400,
            detail="Método deve ser mpesa ou emola."
        )



    pagamento = {

        "carteira":
        "1724330415881x796026612740522000",

        "numero":
        dados.numero,

        "cliente":
        usuario.email,

        "valor":
        str(dados.valor)

    }



    try:

        resposta = requests.post(

            url,

            json=pagamento,

            headers={
                "Content-Type":
                "application/json"
            },

            timeout=30

        )


    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )



    if resposta.status_code != 200:

        raise HTTPException(
            status_code=400,
            detail="Pagamento não confirmado."
        )



    saldo = (
        db.query(Saldo)
        .filter(
            Saldo.usuario_id == dados.usuario_id
        )
        .first()
    )



    if saldo:

        saldo.saldo += dados.valor


    else:

        saldo = Saldo(

            usuario_id=dados.usuario_id,

            saldo=dados.valor

        )

        db.add(saldo)



    db.commit()

    db.refresh(saldo)



    return {

        "message":
        "Recarga efetuada com sucesso.",

        "usuario_id":
        dados.usuario_id,

        "valor":
        dados.valor,

        "saldo_atual":
        saldo.saldo

    }
