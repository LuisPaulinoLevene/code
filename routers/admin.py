from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.admin import Admin
from schemas.admin import (
    AdminCreate,
    AdminUpdate,
    AdminOut
)


router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)



# ==========================
# CREATE
# ==========================

@router.post(
    "/",
    response_model=AdminOut
)
def criar_admin(
    data: AdminCreate,
    db: Session = Depends(get_db)
):

    admin = Admin(
        email=data.email,
        senha=data.senha
    )


    db.add(admin)

    db.commit()

    db.refresh(admin)


    return admin



# ==========================
# READ ALL
# ==========================

@router.get(
    "/",
    response_model=list[AdminOut]
)
def listar_admins(
    db: Session = Depends(get_db)
):

    return (
        db.query(Admin)
        .all()
    )



# ==========================
# READ ONE
# ==========================

@router.get(
    "/{admin_id}",
    response_model=AdminOut
)
def obter_admin(
    admin_id: int,
    db: Session = Depends(get_db)
):

    admin = db.get(
        Admin,
        admin_id
    )


    if not admin:

        raise HTTPException(
            status_code=404,
            detail="Admin não encontrado"
        )


    return admin



# ==========================
# UPDATE
# ==========================

@router.put(
    "/{admin_id}",
    response_model=AdminOut
)
def atualizar_admin(
    admin_id: int,
    data: AdminUpdate,
    db: Session = Depends(get_db)
):

    admin = db.get(
        Admin,
        admin_id
    )


    if not admin:

        raise HTTPException(
            status_code=404,
            detail="Admin não encontrado"
        )



    if data.email is not None:

        admin.email = data.email



    if data.senha is not None:

        admin.senha = data.senha



    db.commit()

    db.refresh(admin)


    return admin



# ==========================
# DELETE
# ==========================

@router.delete(
    "/{admin_id}"
)
def deletar_admin(
    admin_id: int,
    db: Session = Depends(get_db)
):

    admin = db.get(
        Admin,
        admin_id
    )


    if not admin:

        raise HTTPException(
            status_code=404,
            detail="Admin não encontrado"
        )


    db.delete(admin)

    db.commit()


    return {
        "message": "Admin deletado com sucesso"
    }