from pydantic import BaseModel
from typing import Optional


class CalcularCreate(BaseModel):
    usuario_id: int
    imei: str
    marca_id: int
    modelo_id: int



class CalcularResponse(BaseModel):
    imei: str
    marca_id: int
    modelo_id: int
    codigo: str
    saldo_restante: float

    class Config:
        from_attributes = True



class RecargaCreate(BaseModel):
    usuario_id: int
    numero: str
    valor: float
    metodo: str
    referencia: Optional[str] = None

    class Config:
        from_attributes = True