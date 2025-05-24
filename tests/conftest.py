# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.database import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Cria todas as tabelas antes de qualquer teste
    Base.metadata.create_all(bind=engine)
    yield
    # Dropa todas as tabelas ao fim da sessão
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    # Garante que os eventos de startup/shutdown do FastAPI sejam acionados
    with TestClient(app) as c:
        yield c
