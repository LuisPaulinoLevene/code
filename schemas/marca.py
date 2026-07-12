from pydantic import BaseModel, ConfigDict


class MarcaBase(BaseModel):
    marca: str


class MarcaCreate(MarcaBase):
    pass


class MarcaUpdate(MarcaBase):
    pass


class MarcaResponse(MarcaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)