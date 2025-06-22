from sqlalchemy.orm import Session
from src.models import Alimento

def create_alimento(db: Session, *, nome: str,
                    calorias_por_100g: float,
                    proteinas: float,
                    carboidratos: float,
                    gorduras: float) -> Alimento:
    """
    Cria e persiste um novo alimento no banco.
    """
    novo = Alimento(
        nome=nome,
        calorias_por_100g=calorias_por_100g,
        proteinas=proteinas,
        carboidratos=carboidratos,
        gorduras=gorduras
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def get_alimento_by_nome(db: Session, nome: str) -> Alimento | None:
    """
    Retorna o alimento com o nome informado, ou None.
    """
    return db.query(Alimento).filter(Alimento.nome == nome).first()

def update_alimento(db: Session, alimento: Alimento, **kwargs) -> Alimento:
    """
    Atualiza campos do alimento de forma dinâmica.
    Exemplo: update_alimento(db, meu_alimento, proteinas=35)
    """
    for field, value in kwargs.items():
        setattr(alimento, field, value)
    db.commit()
    db.refresh(alimento)
    return alimento

def delete_alimento(db: Session, alimento: Alimento) -> None:
    """
    Remove o alimento do banco.
    """
    db.delete(alimento)
    db.commit()
