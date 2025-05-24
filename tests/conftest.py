import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import src.database as database
from src.database import Base

from fastapi.testclient import TestClient
from src.main import app
from src.api.dependencies import get_db

# --- 1. Fixture autouse para usar um SQLite em memória em TODOS os testes ---
@pytest.fixture(autouse=True)
def setup_in_memory_db():
    """
    Cria engine e SessionLocal em memória, recria as tabelas antes de cada teste
    e as apaga ao final.
    """
    # 1) monta engine em memória
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    # 2) ajusta o módulo database para usar esse engine
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    database.engine = engine
    database.SessionLocal = TestingSessionLocal

    # 3) cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # 4) limpa TODAS as tabelas no fim
    Base.metadata.drop_all(bind=engine)

# --- 2. Override do get_db para o TestClient (integração) ---
def override_get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# --- 3. Fixture do cliente de teste ---
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c