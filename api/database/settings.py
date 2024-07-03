from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import Session
from api.database.tablas import create_tables
from api.settings import db_settings

url = f"{db_settings.username}:{db_settings.password}@{db_settings.url}:{db_settings.port}"
DATABASE_URL = f"postgresql://{url}/{db_settings.name}"

engine = create_engine(DATABASE_URL, echo=db_settings.echo)


def create_database_and_tables(engine_: Engine = None):
    _engine = engine_ or engine
    if not database_exists(_engine.url):
        create_database(_engine.url)
    create_tables(_engine)


def get_session():
    with Session(engine) as session:
        yield session
