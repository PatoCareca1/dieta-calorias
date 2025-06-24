from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models
from ..api import schemas

def get_exercicio(db: Session, exercicio_id: int) -> Optional[models.Exercicio]:
    return db.query(models.Exercicio).filter(models.Exercicio.id == exercicio_id).first()

def get_exercicio_by_nome(db: Session, nome: str) -> Optional[models.Exercicio]:
    return db.query(models.Exercicio).filter(models.Exercicio.nome == nome).first()

def get_exercicios(db: Session, skip: int = 0, limit: int = 100) -> List[models.Exercicio]:
    return db.query(models.Exercicio).offset(skip).limit(limit).all()

def create_exercicio(db: Session, exercicio: schemas.ExercicioCreate) -> models.Exercicio:
    db_exercicio = models.Exercicio(**exercicio.dict())
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio

def update_exercicio(
    db: Session, db_obj: models.Exercicio, obj_in: schemas.ExercicioUpdate
) -> models.Exercicio:
    obj_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        setattr(db_obj, field, obj_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_exercicio(db: Session, id_exercicio: int) -> Optional[models.Exercicio]:
    db_obj = db.query(models.Exercicio).get(id_exercicio)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj