from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    email: EmailStr | None = None
    senha: str | None = None

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True