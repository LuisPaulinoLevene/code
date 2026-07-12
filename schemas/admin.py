from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    email: EmailStr


class AdminCreate(AdminBase):
    senha: str


class AdminUpdate(BaseModel):
    email: EmailStr | None = None
    senha: str | None = None


class AdminOut(AdminBase):
    id: int

    class Config:
        from_attributes = True