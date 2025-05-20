from sqlalchemy.orm import Session
from src.models import ItemRefeicao, Refeicao, Alimento

def create_item_refeicao(db: Session, *, refeicao: Refeicao,
                         alimento: Alimento, quantidade_em_gramas: float) -> ItemRefeicao:
    """
    Cria e persiste um novo item de refeição (ligação refeicao↔alimento).
    """
    novo = ItemRefeicao(
        refeicao=refeicao,
        alimento=alimento,
        quantidade_em_gramas=quantidade_em_gramas
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def get_item_refeicao_by_id(db: Session, id_item: int) -> ItemRefeicao | None:
    """
    Retorna o ItemRefeicao pelo seu id, ou None.
    """
    return db.query(ItemRefeicao).filter(ItemRefeicao.id_item == id_item).first()

def update_item_refeicao(db: Session, item: ItemRefeicao, **kwargs) -> ItemRefeicao:
    """
    Atualiza campos do item de refeição dinamicamente.
    Ex: update_item_refeicao(db, item, quantidade_em_gramas=150)
    """
    for field, value in kwargs.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item

def delete_item_refeicao(db: Session, item: ItemRefeicao) -> None:
    """
    Remove o item de refeição do banco.
    """
    db.delete(item)
    db.commit()
