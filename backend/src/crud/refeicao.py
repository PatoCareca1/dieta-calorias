from datetime import date
from sqlalchemy.orm import Session
from src.models import Refeicao, Usuario

def create_refeicao(db: Session, *, usuario: Usuario,
                    data: date, tipo_refeicao: str) -> Refeicao:
    """
    Cria e persiste uma nova refeição para o usuário.
    """
    nova = Refeicao(
        usuario=usuario,
        data=data,
        tipo_refeicao=tipo_refeicao
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def get_refeicao_by_id(db: Session, id_refeicao: int) -> Refeicao | None:
    """
    Retorna a Refeicao com o id informado, ou None.
    """
    return db.query(Refeicao).filter(Refeicao.id_refeicao == id_refeicao).first()

def update_refeicao(db: Session, refeicao: Refeicao, **kwargs) -> Refeicao:
    """
    Atualiza campos da refeição de forma dinâmica.
    Ex: update_refeicao(db, r, tipo_refeicao="Jantar")
    """
    for field, value in kwargs.items():
        setattr(refeicao, field, value)
    db.commit()
    db.refresh(refeicao)
    return refeicao

def delete_refeicao(db: Session, refeicao: Refeicao) -> None:
    """
    Remove a refeição do banco.
    """
    db.delete(refeicao)
    db.commit()
