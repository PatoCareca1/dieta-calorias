import pytest
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models import Usuario, Alimento, Refeicao, ItemRefeicao
from datetime import date

@pytest.fixture(scope="module")
def db_session():
    # Setup
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    # Teardown
    Base.metadata.drop_all(bind=engine)

def test_criar_usuario(db_session: Session):
    novo_usuario = Usuario(
        nome="Lucas Daniel",
        email="lucas@test.com",
        senha="123456",
        peso=115,
        altura=1.94,
        meta_calorica_diaria=3000
    )
    db_session.add(novo_usuario)
    db_session.commit()

    usuario_banco = db_session.query(Usuario).filter_by(email="lucas@test.com").first()

    assert usuario_banco is not None
    assert usuario_banco.nome == "Lucas Daniel"
    assert usuario_banco.meta_calorica_diaria == 3000

def test_criar_alimento(db_session: Session):
    novo_alimento = Alimento(
        nome="Frango",
        calorias_por_100g=165,
        proteinas=31,
        carboidratos=0,
        gorduras=3.6
    )
    db_session.add(novo_alimento)
    db_session.commit()

    alimento_banco = db_session.query(Alimento).filter_by(nome="Frango").first()

    assert alimento_banco is not None
    assert alimento_banco.proteinas == 31

def test_criar_refeicao_com_item(db_session: Session):
    usuario = db_session.query(Usuario).first()
    alimento = db_session.query(Alimento).first()

    refeicao = Refeicao(
        usuario=usuario,
        data=date.today(),
        tipo_refeicao="Almoço"
    )

    db_session.add(refeicao)
    db_session.commit()

    item_refeicao = ItemRefeicao(
        refeicao=refeicao,
        alimento=alimento,
        quantidade_em_gramas=200
    )

    db_session.add(item_refeicao)
    db_session.commit()

    item_banco = db_session.query(ItemRefeicao).first()

    assert item_banco is not None
    assert item_banco.quantidade_em_gramas == 200
    assert item_banco.alimento.nome == "Frango"
