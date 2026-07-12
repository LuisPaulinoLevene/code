from sqlalchemy import Column, Integer, Float, ForeignKey

from database import Base


class Saldo(Base):
    __tablename__ = "saldos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    saldo = Column(Float, nullable=False, default=0.0)