# Em backend/src/crud/treino.py

from sqlalchemy.orm import Session
from .. import models
# CORREÇÃO: Apontamos para o local correto do schemas (dentro da pasta 'api')
from ..api import schemas

# --- Funções de CRUD para Treino ---

def get_treino(db: Session, treino_id: int):
    """
    Busca um treino específico pelo ID.
    """
    return db.query(models.Treino).filter(models.Treino.id == treino_id).first()

def get_treinos_by_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    """
    Busca todos os treinos de um usuário específico.
    """
    return db.query(models.Treino).filter(models.Treino.usuario_id == usuario_id).offset(skip).limit(limit).all()

def create_treino_for_usuario(db: Session, treino: schemas.TreinoCreate, usuario_id: int):
    """
    Cria um novo treino para um usuário.
    """
    db_treino = models.Treino(**treino.model_dump(), usuario_id=usuario_id)
    db.add(db_treino)
    db.commit()
    db.refresh(db_treino)
    return db_treino


# --- Funções de CRUD para ItemTreino ---

def add_exercicio_to_treino(db: Session, item: schemas.ItemTreinoCreate, treino_id: int):
    """
    Adiciona um exercício a um treino existente.
    """
    db_item_treino = models.ItemTreino(
        **item.model_dump(),
        treino_id=treino_id
    )
    db.add(db_item_treino)
    db.commit()
    db.refresh(db_item_treino)
    return db_item_treino

# --- Funções de CRUD para ItemTreino ---
def get_item_treino(db: Session, item_id: int):
    """
    Busca um item de treino específico pelo seu ID.
    """
    return db.query(models.ItemTreino).filter(models.ItemTreino.id == item_id).first()

def delete_item_treino(db: Session, item_id: int):
    """
    Deleta um item de treino do banco de dados.
    """
    db_item = get_item_treino(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item