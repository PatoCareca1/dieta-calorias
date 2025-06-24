# src/api/routers/treinos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ... import crud, models
from src.api import schemas
from ..dependencies import get_db
# 1. Importando as duas funções de segurança necessárias do local correto
from ..security import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/treinos",
    tags=["Treinos"],
    responses={404: {"description": "Não encontrado"}},
)

# 2. ENDPOINT ADICIONADO para o administrador visualizar todos os treinos
@router.get("/all/", response_model=List[schemas.Treino])
def read_all_treinos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: models.Usuario = Depends(get_current_admin_user)
):
    """
    (Admin) Retorna uma lista de todos os treinos de todos os usuários.
    """
    treinos = crud.treino.get_treinos(db, skip=skip, limit=limit)
    return treinos


@router.post("/", response_model=schemas.Treino, status_code=status.HTTP_201_CREATED)
def create_treino(
    treino: schemas.TreinoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Cria um novo plano de treino para o usuário logado.
    """
    return crud.treino.create_treino_for_usuario(
        db=db, treino=treino, usuario_id=current_user.id
    )

@router.get("/", response_model=List[schemas.Treino])
def read_treinos_do_usuario(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Retorna todos os planos de treino do usuário logado.
    """
    treinos = crud.treino.get_treinos_by_usuario(
        db, usuario_id=current_user.id, skip=skip, limit=limit
    )
    return treinos

@router.get("/{treino_id}", response_model=schemas.Treino)
def read_treino(
    treino_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Retorna um plano de treino específico com todos os seus exercícios.
    """
    db_treino = crud.treino.get_treino(db, treino_id=treino_id)
    if db_treino is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    if db_treino.usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não permitido")
        
    return db_treino

@router.post("/{treino_id}/exercicios/", response_model=schemas.ItemTreino, status_code=status.HTTP_201_CREATED)
def add_exercicio_a_treino(
    treino_id: int,
    item: schemas.ItemTreinoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Adiciona um exercício a um plano de treino existente.
    """
    db_treino = crud.treino.get_treino(db, treino_id=treino_id)
    if db_treino is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    if db_treino.usuario_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não permitido")
    
    db_exercicio = crud.exercicio.get_exercicio(db, exercicio_id=item.exercicio_id)
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    return crud.treino.add_exercicio_to_treino(db=db, item=item, treino_id=treino_id)

@router.delete("/{treino_id}/exercicios/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_exercicio_do_treino(
    treino_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Remove um exercício de um plano de treino.
    """
    db_treino = crud.treino.get_treino(db, treino_id=treino_id)
    if not db_treino or db_treino.usuario_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treino não encontrado")

    db_item = crud.treino.get_item_treino(db, item_id=item_id)
    if not db_item or db_item.treino_id != db_treino.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado neste treino")
    
    crud.treino.delete_item_treino(db, item_id=item_id)
    return None