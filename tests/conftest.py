import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import src.database as database
from src.database import Base

from fastapi.testclient import TestClient
from src.main import app
from src.api.dependencies import get_db

# 1) Banco em memória em TODOS os testes
@pytest.fixture(autouse=True)
def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    database.engine = engine
    database.SessionLocal = TestingSessionLocal
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 2) Override do get_db para o TestClient
def override_get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3) Cliente de teste para integração
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# 4) SESSÃO de teste para fixtures que precisam de db direto
@pytest.fixture
def db():
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()
