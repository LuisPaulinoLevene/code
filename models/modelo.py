from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Modelo(Base):

    __tablename__ = "modelos"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    modelo = Column(
        String,
        nullable=False
    )


    formula = Column(
        Integer,
        nullable=False
    )


    marca_id = Column(
        Integer,
        ForeignKey("marcas.id"),
        nullable=False
    )


    marca = relationship(
        "Marca",
        back_populates="modelos"
    )