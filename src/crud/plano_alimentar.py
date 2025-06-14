from sqlalchemy.orm import Session
from datetime import date

from src import models
from src.api import schemas

def get_plano_alimentar_by_usuario_id(db: Session, usuario_id: int) -> models.PlanoAlimentar | None:
    """
    Retorna o plano alimentar de um usuário específico.
    """
    return db.query(models.PlanoAlimentar).filter(models.PlanoAlimentar.usuario_id == usuario_id).first()

def create_or_update_plano_alimentar(
    db: Session, 
    plano_in: schemas.PlanoAlimentarCreate, 
    usuario_id: int
) -> models.PlanoAlimentar:
    """
    Cria um novo plano alimentar para um usuário ou atualiza o existente.
    Este padrão é conhecido como "upsert" (update or insert).
    """
    # Verifica se já existe um plano para este usuário
    db_plano = get_plano_alimentar_by_usuario_id(db, usuario_id=usuario_id)

    if db_plano:
        # Se existe, atualiza os campos
        print(f"Atualizando plano alimentar existente para o usuário ID: {usuario_id}")
        update_data = plano_in.dict()
        for field, value in update_data.items():
            setattr(db_plano, field, value)
        db_plano.data_criacao = date.today() # Atualiza a data
    else:
        # Se não existe, cria um novo
        print(f"Criando novo plano alimentar para o usuário ID: {usuario_id}")
        db_plano = models.PlanoAlimentar(
            **plano_in.dict(), 
            usuario_id=usuario_id
        )
        db.add(db_plano)
    
    db.commit()
    db.refresh(db_plano)
    return db_plano
