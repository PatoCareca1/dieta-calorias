# Em backend/src/crud/exercicio.py

from sqlalchemy.orm import Session
from .. import models
# CORREÇÃO: Apontamos para o local correto do schemas (dentro da pasta 'api')
from ..api import schemas

def get_exercicio(db: Session, exercicio_id: int):
    """
    Busca um único exercício pelo seu ID.
    """
    return db.query(models.Exercicio).filter(models.Exercicio.id == exercicio_id).first()

def get_exercicio_by_nome(db: Session, nome: str):
    """
    Busca um único exercício pelo seu nome. Útil para evitar duplicatas.
    """
    return db.query(models.Exercicio).filter(models.Exercicio.nome == nome).first()

def get_exercicios(db: Session, skip: int = 0, limit: int = 100):
    """
    Busca uma lista de exercícios com paginação.
    """
    return db.query(models.Exercicio).offset(skip).limit(limit).all()

def create_exercicio(db: Session, exercicio: schemas.ExercicioCreate):
    """
    Cria um novo exercício no banco de dados.
    """
    db_exercicio = models.Exercicio(
        nome=exercicio.nome,
        grupo_muscular=exercicio.grupo_muscular,
        descricao=exercicio.descricao
    )
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio