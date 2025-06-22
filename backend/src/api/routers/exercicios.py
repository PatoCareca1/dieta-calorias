# Em backend/src/api/routers/exercicios.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ... import crud, models
from .. import schemas # Renomeei na minha mente para api_schemas, mas o seu é schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/exercicios",
    tags=["exercicios"],
    responses={404: {"description": "Não encontrado"}},
)

@router.post("/", response_model=schemas.Exercicio, status_code=status.HTTP_201_CREATED)
def create_exercicio(
    exercicio: schemas.ExercicioCreate, db: Session = Depends(get_db)
):
    """
    Cria um novo exercício no banco de dados.
    - **nome**: Nome do exercício (deve ser único).
    - **grupo_muscular**: Grupo muscular alvo.
    - **descricao**: Descrição opcional de como executar o exercício.
    """
    db_exercicio = crud.exercicio.get_exercicio_by_nome(db, nome=exercicio.nome)
    if db_exercicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um exercício com este nome já existe."
        )
    return crud.exercicio.create_exercicio(db=db, exercicio=exercicio)


@router.get("/", response_model=List[schemas.Exercicio])
def read_exercicios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista de todos os exercícios cadastrados.
    """
    exercicios = crud.exercicio.get_exercicios(db, skip=skip, limit=limit)
    return exercicios


@router.get("/{exercicio_id}", response_model=schemas.Exercicio)
def read_exercicio(exercicio_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um exercício específico pelo seu ID.
    """
    db_exercicio = crud.exercicio.get_exercicio(db, exercicio_id=exercicio_id)
    if db_exercicio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado."
        )
    return db_exercicio