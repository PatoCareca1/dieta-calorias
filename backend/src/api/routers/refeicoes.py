# src/api/routers/refeicoes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src import models
from src.api import schemas
from src.crud import refeicao as crud_refeicao
from src.api.dependencies import get_db
# 1. Importando as funções de segurança do local correto
from src.api.security import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/refeicoes", 
    tags=["Refeições"]
)

# 2. ENDPOINT ADICIONADO para o administrador visualizar todas as refeições
@router.get("/", response_model=List[schemas.RefeicaoRead])
def read_all_refeicoes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.Usuario = Depends(get_current_admin_user)
):
    """
    (Admin) Retorna uma lista de todas as refeições de todos os usuários.
    """
    refeicoes = crud_refeicao.get_refeicoes(db, skip=skip, limit=limit)
    return refeicoes

# 3. ENDPOINT AJUSTADO: Criar uma refeição para o usuário LOGADO
@router.post("/", response_model=schemas.RefeicaoRead, status_code=status.HTTP_201_CREATED)
def create_refeicao_for_current_user(
    refeicao_in: schemas.RefeicaoCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Cria uma nova refeição para o usuário autenticado.
    """
    return crud_refeicao.create_refeicao_for_user(db=db, refeicao_in=refeicao_in, usuario_id=current_user.id)

# 4. ENDPOINT AJUSTADO: Buscar uma refeição específica com validação de permissão
@router.get("/{refeicao_id}", response_model=schemas.RefeicaoRead)
def read_refeicao(
    refeicao_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Busca uma refeição específica. Um usuário só pode ver suas próprias refeições.
    """
    db_refeicao = crud_refeicao.get_refeicao(db, refeicao_id=refeicao_id)
    if db_refeicao is None:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    if db_refeicao.usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não permitido")
    return db_refeicao

# 5. ENDPOINT AJUSTADO: Atualizar uma refeição com validação de permissão
@router.put("/{refeicao_id}", response_model=schemas.RefeicaoRead)
def update_refeicao(
    refeicao_id: int, 
    refeicao_in: schemas.RefeicaoUpdate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Atualiza uma refeição. Um usuário só pode atualizar suas próprias refeições.
    """
    db_refeicao = crud_refeicao.get_refeicao(db, refeicao_id=refeicao_id)
    if db_refeicao is None:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    if db_refeicao.usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não permitido")
    return crud_refeicao.update_refeicao(db, db_obj=db_refeicao, obj_in=refeicao_in)

# 6. ENDPOINT AJUSTADO: Deletar uma refeição com validação de permissão
@router.delete("/{refeicao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_refeicao(
    refeicao_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Deleta uma refeição. Um usuário só pode deletar suas próprias refeições.
    """
    db_refeicao = crud_refeicao.get_refeicao(db, refeicao_id=refeicao_id)
    if db_refeicao is None:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    if db_refeicao.usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não permitido")
    crud_refeicao.delete_refeicao(db, id_refeicao=refeicao_id)
    return None