from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models.usuario import Usuario

from schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioOut
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)



# ==========================
# CREATE
# ==========================

@router.post(
    "/",
    response_model=UsuarioOut
)
def criar_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db)
):

    existente = (
        db.query(Usuario)
        .filter(
            Usuario.email == data.email
        )
        .first()
    )


    if existente:

        raise HTTPException(
            status_code=400,
            detail="Este email já está cadastrado."
        )



    usuario = Usuario(
        email=data.email,
        senha=data.senha
    )


    db.add(usuario)

    db.commit()

    db.refresh(usuario)


    return usuario





# ==========================
# LOGIN
# ==========================

@router.post("/login")
def login_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db)
):


    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.email == data.email,
            Usuario.senha == data.senha
        )
        .first()
    )



    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )



    return {

        "message": "Usuário logado com sucesso",

        "id": usuario.id,

        "email": usuario.email

    }







# ==========================
# READ ALL
# ==========================

@router.get(
    "/",
    response_model=list[UsuarioOut]
)
def listar_usuarios(
    db: Session = Depends(get_db)
):

    return (
        db.query(Usuario)
        .all()
    )







# ==========================
# READ ONE
# ==========================

@router.get(
    "/{usuario_id}",
    response_model=UsuarioOut
)
def obter_usuario(
    usuario_id:int,
    db: Session = Depends(get_db)
):

    usuario = db.get(
        Usuario,
        usuario_id
    )


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )


    return usuario







# ==========================
# UPDATE
# ==========================

@router.put(
    "/{usuario_id}",
    response_model=UsuarioOut
)
def atualizar_usuario(
    usuario_id:int,
    data:UsuarioUpdate,
    db:Session = Depends(get_db)
):


    usuario = db.get(
        Usuario,
        usuario_id
    )


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )



    if data.email is not None:

        usuario.email = data.email



    if data.senha is not None:

        usuario.senha = data.senha




    db.commit()

    db.refresh(usuario)


    return usuario







# ==========================
# DELETE
# ==========================

@router.delete(
    "/{usuario_id}"
)
def deletar_usuario(
    usuario_id:int,
    db:Session = Depends(get_db)
):


    usuario = db.get(
        Usuario,
        usuario_id
    )


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )



    db.delete(usuario)

    db.commit()



    return {

        "message":
        "Usuário deletado com sucesso"

    }