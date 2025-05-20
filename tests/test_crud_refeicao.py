import pytest
from datetime import date
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.crud.usuario import create_user
from src.crud.refeicao import (
    create_refeicao,
    get_refeicao_by_id,
    update_refeicao,
    delete_refeicao
)
from src.models import Refeicao

@pytest.fixture(scope="module")
def db():
    # setup
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    # teardown
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_refeicao(db: Session):
    # primeiro, crio um usuário para associar
    user = create_user(db,
        nome="Teste Ref", email="refeicao@teste.com", senha="abc123",
        peso=70, altura=1.75, meta_calorica_diaria=2500
    )
    r = create_refeicao(db,
        usuario=user,
        data=date.today(),
        tipo_refeicao="Almoço"
    )
    fetched = get_refeicao_by_id(db, r.id_refeicao)
    assert fetched is not None
    assert isinstance(fetched, Refeicao)
    assert fetched.tipo_refeicao == "Almoço"

def test_update_refeicao(db: Session):
    r = db.query(Refeicao).first()
    updated = update_refeicao(db, r, tipo_refeicao="Jantar")
    assert updated.tipo_refeicao == "Jantar"

def test_delete_refeicao(db: Session):
    r = db.query(Refeicao).first()
    delete_refeicao(db, r)
    assert get_refeicao_by_id(db, r.id_refeicao) is None
