import pytest
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.crud.usuario import create_user, get_user_by_email, update_user, delete_user
from src.models import Usuario

@pytest.fixture(scope="module")
def db():
    # setup
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_user(db: Session):
    u = create_user(db,
        nome="Ana Silva", email="ana@teste.com", senha="senha123",
        peso=60, altura=1.65, meta_calorica_diaria=2000
    )
    assert isinstance(u, Usuario)
    fetched = get_user_by_email(db, "ana@teste.com")
    assert fetched.id_usuario == u.id_usuario

def test_update_user(db: Session):
    u = get_user_by_email(db, "ana@teste.com")
    updated = update_user(db, u, peso=62, meta_calorica_diaria=2100)
    assert updated.peso == 62
    assert updated.meta_calorica_diaria == 2100

def test_delete_user(db: Session):
    u = get_user_by_email(db, "ana@teste.com")
    delete_user(db, u)
    assert get_user_by_email(db, "ana@teste.com") is None
