from pydantic import BaseModel, ConfigDict, Field


class SaldoBase(BaseModel):
    usuario_id: int
    saldo: float = Field(..., ge=0)


class SaldoCreate(SaldoBase):
    pass


class SaldoUpdate(BaseModel):
    saldo: float = Field(..., ge=0)


class SaldoResponse(SaldoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)