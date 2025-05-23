import pytest
from datetime import date
from sqlalchemy.orm import Session
from src.models import Usuario, Alimento, Refeicao, ItemRefeicao
from src.services.calculadora_calorias import (
    calcular_calorias_item,
    calcular_calorias_refeicao,
    calcular_calorias_por_dia,
    avaliar_consumo_diario
)

@pytest.fixture
def exemplo_entidades(db: Session):
    # cria um usuário com meta 1000 kcal
    user = Usuario(
        nome="Teste Calorias",
        email="calorias@teste.com",
        senha="pwd",
        peso=70,
        altura=1.75,
        meta_calorica_diaria=1000
    )
    db.add(user)

    # cria dois alimentos diferentes
    arroz = Alimento(nome="Arroz", calorias_por_100g=130, proteinas=2.7, carboidratos=28, gorduras=0.3)
    banana = Alimento(nome="Banana", calorias_por_100g=89, proteinas=1.1, carboidratos=23, gorduras=0.3)
    db.add_all([arroz, banana])
    db.commit()

    # cria uma refeição com dois itens
    refeicao = Refeicao(usuario=user, data=date.today(), tipo_refeicao="Teste")
    db.add(refeicao)
    db.commit()

    # item 1: 200g de arroz → 200 * 130 / 100 = 260 kcal
    item1 = ItemRefeicao(refeicao=refeicao, alimento=arroz, quantidade_em_gramas=200)
    # item 2: 150g de banana → 150 * 89 / 100 = 133.5 kcal
    item2 = ItemRefeicao(refeicao=refeicao, alimento=banana, quantidade_em_gramas=150)
    db.add_all([item1, item2])
    db.commit()

    return {
        "user": user,
        "refeicao": refeicao,
        "item1": item1,
        "item2": item2
    }

def test_calcular_calorias_item(exemplo_entidades):
    item1 = exemplo_entidades["item1"]
    assert pytest.approx(calcular_calorias_item(item1), rel=1e-3) == 260.0

    item2 = exemplo_entidades["item2"]
    assert pytest.approx(calcular_calorias_item(item2), rel=1e-3) == 133.5

def test_calcular_calorias_refeicao(exemplo_entidades):
    refeicao = exemplo_entidades["refeicao"]
    total = calcular_calorias_refeicao(refeicao)
    assert pytest.approx(total, rel=1e-3) == 393.5

def test_calcular_calorias_por_dia(db, exemplo_entidades):
    user = exemplo_entidades["user"]
    total_dia = calcular_calorias_por_dia(db, user, date.today())
    assert pytest.approx(total_dia, rel=1e-3) == 393.5

def test_avalidar_consumo_diario(exemplo_entidades):
    user = exemplo_entidades["user"]
    # meta 1000, consumo 393.5 → abaixo
    assert avaliar_consumo_diario(user, 393.5) == "abaixo"
    # meta 1000, consumo igual → dentro
    assert avaliar_consumo_diario(user, 1000.0) == "dentro"
    # meta 1000, consumo acima → acima
    assert avaliar_consumo_diario(user, 1200.0) == "acima"
