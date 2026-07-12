from pydantic import BaseModel


class ModeloCreate(BaseModel):

    modelo: str
    formula: int
    marca_id: int



class ModeloUpdate(BaseModel):

    modelo: str
    formula: int
    marca_id: int



class ModeloResponse(BaseModel):

    id: int
    modelo: str
    formula: int
    marca_id: int


    class Config:
        from_attributes = True