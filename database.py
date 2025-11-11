# import contextlib

from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
SQLALCHEMY_DATABASE_URL_psdb = config('SQLALCHEMY_DATABASE_URL_psdb')
SQLALCHEMY_DATABASE_URL_lite = config('SQLALCHEMY_DATABASE_URL_lite')
#SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"


engine_lite = create_engine(
        SQLALCHEMY_DATABASE_URL_lite, connect_args={"check_same_thread": False})
SessionLocal_lite = sessionmaker(autocommit=False, autoflush=False, bind=engine_lite)

engine_ps = create_engine(SQLALCHEMY_DATABASE_URL_psdb)
SessionLocal_ps = sessionmaker(autocommit=False, autoflush=False, bind=engine_ps)

Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

# @contextlib.contextmanager
def get_ps_db():
    db = SessionLocal_ps()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()

def get_lite_db():
    db = SessionLocal_lite()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()