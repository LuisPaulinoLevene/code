from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Marca(Base):

    __tablename__ = "marcas"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    marca = Column(
        String,
        unique=True,
        nullable=False
    )


    modelos = relationship(
        "Modelo",
        back_populates="marca"
    )