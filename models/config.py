from sqlalchemy import Column, Integer, Float

from database import Base


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    preco_codigo = Column(Float, nullable=False, default=0.0)