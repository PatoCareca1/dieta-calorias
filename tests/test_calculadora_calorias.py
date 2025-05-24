# src/services/calculadora_calorias.py

from datetime import date
from sqlalchemy.orm import Session
from src.models import Refeicao, ItemRefeicao

def calcular_calorias_item(item: ItemRefeicao) -> float:
    """
    Retorna as calorias de um ItemRefeicao:
      quantidade_em_gramas * calorias_por_100g / 100
    """
    return item.quantidade_em_gramas * item.alimento.calorias_por_100g / 100.0

def calcular_calorias_refeicao(refeicao: Refeicao) -> float:
    """
    Soma as calorias de todos os itens de uma refeição.
    """
    return sum(calcular_calorias_item(item) for item in refeicao.itens_refeicao)

def calcular_calorias_por_dia(
    db: Session,
    usuario: Refeicao.usuario,  # ou Usuario
    dia: date
) -> float:
    """
    Soma as calorias de todas as refeições de um usuário em uma data.
    """
    refeicoes = (
        db.query(Refeicao)
          .filter(
              Refeicao.id_usuario == usuario.id_usuario,
              Refeicao.data == dia
          )
          .all()
    )
    total = 0.0
    for ref in refeicoes:
        total += calcular_calorias_refeicao(ref)
    return total

def avaliar_consumo_diario(usuario, total: float) -> str:
    """
    Compara o total de calorias ingeridas com a meta do usuário,
    retornando "abaixo", "dentro" ou "acima".
    """
    meta = usuario.meta_calorica_diaria
    if total < meta:
        return "abaixo"
    elif total == meta:
        return "dentro"
    else:
        return "acima"
