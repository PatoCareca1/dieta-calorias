import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database import Base, get_db, engine, SessionLocal, database
from src.database import DATABASE_URL

# Vamos usar um SQLite em memória só para os testes de integração
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(autouse=True)
def setup_in_memory_db():
    """
    Para cada teste, sobrescreve o engine/SessionLocal
    para um SQLite em memória, recria e depois dropa as tabelas.
    """
    # cria engine em memória
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    # ajusta o módulo database para usar esse engine
    database.engine = engine
    database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # cria tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # limpa ao final
    Base.metadata.drop_all(bind=engine)

# Sobrescreve a dependência de get_db para usar nossa sessão de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Cria todas as tabelas antes de começar
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # E derruba tudo quando acabar
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    # cria as tabelas
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    # limpa após os testes
    Base.metadata.drop_all(bind=engine)