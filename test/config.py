import json
from unittest import mock

import pytest
from pathlib import Path
from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session
from importlib import import_module
from fastapi.testclient import TestClient

from api.authenticacion.token import get_current_user
from api.database.tablas import create_tables
from api.app import app


def load_testing_data(engine: Engine):
    """
    Carga datos JSON en una base de datos SQLite en memoria usando SQLModel.

    Args:
    Returns:
        None
    """
    create_tables(engine)
    with Session(engine) as session:
        seed_path = Path(__file__).parent / "seed"
        # Cargar datos JSON en las tablas
        for file in seed_path.iterdir():
            if file.is_file() and file.suffix == ".json":
                table_name = file.stem.capitalize()

            # Importar modelo correspondiente
            try:
                models = import_module("api.database.tablas")
                model = getattr(models, table_name)
            except (ImportError, AttributeError):
                raise ValueError(f"No existe modelo para la tabla: {table_name}")

            # Cargar datos JSON del archivo
            with file.open("r") as f:
                db_data = json.load(f)

            # Insertar datos en la tabla correspondiente
            for data in db_data:
                model_object = model(**data)
                session.add(model_object)
        session.commit()


@pytest.fixture(scope="session")
def test_client():
    db_path = Path("test.db")
    if db_path.exists():
        db_path.unlink()

    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

    # Habilitar restricciones de claves foráneas
    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    load_testing_data(engine)
    app.dependency_overrides[get_current_user] = lambda: "TEST"
    with mock.patch("api.database.settings.engine", engine):
        with TestClient(app) as client:
            yield client

    db_file = Path(__file__).parent / "test.db"
    db_file.unlink()
