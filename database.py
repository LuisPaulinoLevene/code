from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


DATABASE_URL = config("DATABASE_URL")


if DATABASE_URL.startswith("postgres://"):

    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg2://",
        1
    )


elif DATABASE_URL.startswith("postgresql://"):

    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1
    )


engine = create_engine(
    DATABASE_URL,
    echo=True
)


Base = declarative_base()
