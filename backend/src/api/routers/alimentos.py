from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.crud import alimento as crud_alimento
from src import models
from src.api import schemas
from src.api.dependencies import get_db
# 1. Importando a função de segurança do local correto
from src.api.security import get_current_admin_user 

router = APIRouter(
    prefix="/alimentos", 
    tags=["Alimentos"],
    # 2. Protegendo todos os endpoints deste router para serem acessíveis apenas por admin
    dependencies=[Depends(get_current_admin_user)]
)

@router.get("/", response_model=List[schemas.AlimentoRead])
def read_alimentos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.Usuario = Depends(get_current_admin_user)
):
    """
    (Admin) Retorna uma lista de todos os alimentos cadastrados no sistema.
    """
    alimentos = crud_alimento.get_alimentos(db, skip=skip, limit=limit)
    return alimentos

@router.post("/", response_model=schemas.AlimentoRead, status_code=status.HTTP_201_CREATED)
def create_alimento(
    alimento_in: schemas.AlimentoCreate, 
    db: Session = Depends(get_db)
):
    """
    (Admin) Cria um novo alimento no banco de dados.
    """
    if crud_alimento.get_alimento_by_nome(db, nome=alimento_in.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alimento com este nome já cadastrado."
        )
    return crud_alimento.create_alimento(db=db, alimento_in=alimento_in)

@router.get("/{alimento_id}", response_model=schemas.AlimentoRead)
def read_alimento(alimento_id: int, db: Session = Depends(get_db)):
    """
    (Admin) Retorna os detalhes de um alimento específico.
    """
    db_alimento = crud_alimento.get_alimento(db, alimento_id=alimento_id)
    if db_alimento is None:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return db_alimento

@router.put("/{alimento_id}", response_model=schemas.AlimentoRead)
def update_alimento(
    alimento_id: int,
    alimento_in: schemas.AlimentoUpdate,
    db: Session = Depends(get_db)
):
    """
    (Admin) Atualiza um alimento existente.
    """
    db_alimento = crud_alimento.get_alimento(db, alimento_id=alimento_id)
    if db_alimento is None:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return crud_alimento.update_alimento(db=db, db_obj=db_alimento, obj_in=alimento_in)

@router.delete("/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alimento(alimento_id: int, db: Session = Depends(get_db)):
    """
    (Admin) Deleta um alimento.
    """
    db_alimento = crud_alimento.get_alimento(db, alimento_id=alimento_id)
    if db_alimento is None:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    
    # 3. Correção do bug: passando o objeto para a função de deletar
    crud_alimento.delete_alimento(db=db, id_alimento=alimento_id)
    return None