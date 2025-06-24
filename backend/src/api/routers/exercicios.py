from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src import models
from src.api import schemas
from src.crud import exercicio as crud_exercicio
from src.api.dependencies import get_db
from src.api.security import get_current_admin_user

router = APIRouter(
    prefix="/exercicios",
    tags=["Exercícios"],
    dependencies=[Depends(get_current_admin_user)],
    responses={404: {"description": "Não encontrado"}},
)

@router.post("/", response_model=schemas.Exercicio, status_code=status.HTTP_201_CREATED)
def create_exercicio(exercicio: schemas.ExercicioCreate, db: Session = Depends(get_db)):
    db_exercicio = crud_exercicio.get_exercicio_by_nome(db, nome=exercicio.nome)
    if db_exercicio:
        raise HTTPException(status_code=400, detail="Um exercício com este nome já existe.")
    return crud_exercicio.create_exercicio(db=db, exercicio=exercicio)

@router.get("/", response_model=List[schemas.Exercicio])
def read_exercicios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exercicios = crud_exercicio.get_exercicios(db, skip=skip, limit=limit)
    return exercicios

@router.get("/{exercicio_id}", response_model=schemas.Exercicio)
def read_exercicio(exercicio_id: int, db: Session = Depends(get_db)):
    db_exercicio = crud_exercicio.get_exercicio(db, exercicio_id=exercicio_id)
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")
    return db_exercicio

@router.put("/{exercicio_id}", response_model=schemas.Exercicio)
def update_exercicio(
    exercicio_id: int,
    exercicio_in: schemas.ExercicioUpdate,
    db: Session = Depends(get_db)
):
    """
    (Admin) Atualiza um exercício existente.
    """
    db_exercicio = crud_exercicio.get_exercicio(db, exercicio_id=exercicio_id)
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return crud_exercicio.update_exercicio(db=db, db_obj=db_exercicio, obj_in=exercicio_in)

@router.delete("/{exercicio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercicio(exercicio_id: int, db: Session = Depends(get_db)):
    """
    (Admin) Deleta um exercício.
    """
    db_exercicio = crud_exercicio.get_exercicio(db, exercicio_id=exercicio_id)
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    crud_exercicio.delete_exercicio(db=db, id_exercicio=exercicio_id)
    return None