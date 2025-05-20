import pytest
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.crud.alimento import (
    create_alimento,
    get_alimento_by_nome,
    update_alimento,
    delete_alimento
)
from src.models import Alimento

@pytest.fixture(scope="module")
def db():
    # setup: criar tabelas
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    # teardown: dropar tabelas
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_alimento(db: Session):
    a = create_alimento(db,
        nome="Arroz",
        calorias_por_100g=130,
        proteinas=2.7,
        carboidratos=28,
        gorduras=0.3
    )
    assert isinstance(a, Alimento)
    fetched = get_alimento_by_nome(db, "Arroz")
    assert fetched.id_alimento == a.id_alimento
    assert fetched.calorias_por_100g == 130

def test_update_alimento(db: Session):
    a = get_alimento_by_nome(db, "Arroz")
    updated = update_alimento(db, a, proteinas=3.0, gorduras=0.5)
    assert updated.proteinas == 3.0
    assert updated.gorduras == 0.5

def test_delete_alimento(db: Session):
    a = get_alimento_by_nome(db, "Arroz")
    delete_alimento(db, a)
    assert get_alimento_by_nome(db, "Arroz") is None
