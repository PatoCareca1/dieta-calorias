# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import src.database as database
from src.database import Base

@pytest.fixture(autouse=True)
def setup_in_memory_db():
    """
    Antes de cada teste:
     - cria um engine in-memory
     - substitui o engine e o SessionLocal do seu código
     - recria todo o esquema (drop + create)
    """
    # 1) cria engine fresh em memória
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )

    # 2) override no módulo src.database
    database.engine = test_engine
    database.SessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False
    )

    # 3) drop/cria esquema limpo
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield
    # (não precisa dropar depois, a memória some ao final de cada teste)

@pytest.fixture
def db():
    """
    Sessão que seus testes vão usar.
    """
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()
