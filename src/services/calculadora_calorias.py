from datetime import date
from sqlalchemy.orm import Session
from src.models import ItemRefeicao, Refeicao, Usuario

def calcular_calorias_item(item: ItemRefeicao) -> float:
    """
    Calcula as calorias de um item de refeição:
    (quantidade_em_gramas * calorias_por_100g) / 100
    """
    return item.quantidade_em_gramas * item.alimento.calorias_por_100g / 100.0

def calcular_calorias_refeicao(refeicao: Refeicao) -> float:
    """
    Soma as calorias de todos os itens de uma refeição.
    """
    return sum(calcular_calorias_item(item) for item in refeicao.itens_refeicao)

def calcular_calorias_por_dia(db: Session, usuario: Usuario, dia: date) -> float:
    """
    Busca todas as refeições de um usuário em um dia e soma suas calorias.
    """
    refeicoes = (
        db.query(Refeicao)
          .filter(
              Refeicao.id_usuario == usuario.id_usuario,
              Refeicao.data == dia
          )
          .all()
    )
    return sum(calcular_calorias_refeicao(r) for r in refeicoes)

def avaliar_consumo_diario(usuario: Usuario, total_calorias: float) -> str:
    """
    Compara o total ingerido com a meta e retorna:
    - "abaixo" se < meta
    - "dentro" se == meta
    - "acima" se > meta
    """
    if total_calorias < usuario.meta_calorica_diaria:
        return "abaixo"
    if total_calorias > usuario.meta_calorica_diaria:
        return "acima"
    return "dentro"
