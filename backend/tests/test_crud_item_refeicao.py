import pytest
from datetime import date
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.crud.usuario import create_user
from src.crud.alimento import create_alimento
from src.crud.refeicao import create_refeicao
from src.crud.item_refeicao import (
    create_item_refeicao,
    get_item_refeicao_by_id,
    update_item_refeicao,
    delete_item_refeicao
)
from src.models import ItemRefeicao

@pytest.fixture(scope="module")
def db():
    # setup: cria tabelas
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    # teardown: dropa tabelas
    Base.metadata.drop_all(bind=engine)

def test_create_and_get_item(db: Session):
    # precondições: usuário, alimento e refeição existem
    user = create_user(db,
        nome="Teste Item", email="item@teste.com", senha="abc",
        peso=65, altura=1.70, meta_calorica_diaria=2200
    )
    alim = create_alimento(db,
        nome="Banana", calorias_por_100g=89,
        proteinas=1.1, carboidratos=23, gorduras=0.3
    )
    refeicao = create_refeicao(db,
        usuario=user, data=date.today(),
        tipo_refeicao="Lanche"
    )

    item = create_item_refeicao(db,
        refeicao=refeicao,
        alimento=alim,
        quantidade_em_gramas=120
    )
    assert isinstance(item, ItemRefeicao)

    fetched = get_item_refeicao_by_id(db, item.id_item)
    assert fetched is not None
    assert fetched.quantidade_em_gramas == 120
    assert fetched.alimento.nome == "Banana"

def test_update_item(db: Session):
    item = db.query(ItemRefeicao).first()
    updated = update_item_refeicao(db, item, quantidade_em_gramas=150)
    assert updated.quantidade_em_gramas == 150

def test_delete_item(db: Session):
    item = db.query(ItemRefeicao).first()
    delete_item_refeicao(db, item)
    assert get_item_refeicao_by_id(db, item.id_item) is None
