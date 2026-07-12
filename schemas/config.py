from pydantic import BaseModel, ConfigDict, Field


class ConfigBase(BaseModel):
    preco_codigo: float = Field(..., gt=0)


class ConfigCreate(ConfigBase):
    pass


class ConfigUpdate(ConfigBase):
    pass


class ConfigResponse(ConfigBase):
    id: int

    model_config = ConfigDict(from_attributes=True)