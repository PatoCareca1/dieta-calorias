from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src import models
from src.api import schemas
from src.crud import usuario as crud_usuario
# Ajuste a importação de get_db e get_simulated_current_user conforme onde você as definiu
from src.api.dependencies import get_db, get_simulated_current_user 

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    responses={404: {"description": "Não encontrado"}},
)

@router.post("/", response_model=schemas.UsuarioRead, status_code=status.HTTP_201_CREATED)
def api_create_user(
    usuario_in: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    db_user_by_email = crud_usuario.get_usuario_by_email(db, email=usuario_in.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está registrado."
        )
    created_user = crud_usuario.create_usuario(db=db, usuario=usuario_in)
    return created_user

@router.get("/me/", response_model=schemas.UsuarioRead)
def api_get_current_user_me(
    current_user: models.Usuario = Depends(get_simulated_current_user) # Usando a dependência simulada
):
    """
    Obtém os dados do perfil do usuário "atualmente autenticado" (simulado).
    """
    return current_user # A dependência já retorna o objeto models.Usuario

@router.get("/{usuario_id}", response_model=schemas.UsuarioRead)
def api_get_user(
    usuario_id: int, 
    db: Session = Depends(get_db)
    # current_user: models.Usuario = Depends(get_simulated_current_user) # Exemplo de proteção
):
    # Lógica de permissão (exemplo):
    # if usuario_id != current_user.id and not current_user.is_admin: # Supondo um campo is_admin
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado")
    
    db_user = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return db_user

@router.put("/{usuario_id}", response_model=schemas.UsuarioRead)
def api_update_user(
    usuario_id: int,
    usuario_in: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    # current_user: models.Usuario = Depends(get_simulated_current_user) # Exemplo de proteção
):
    db_user = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Lógica de permissão (exemplo):
    # if db_user.id != current_user.id and not current_user.is_admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a atualizar este usuário")

    if usuario_in.email and usuario_in.email != db_user.email:
        existing_user_by_email = crud_usuario.get_usuario_by_email(db, email=usuario_in.email)
        if existing_user_by_email and existing_user_by_email.id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail já está registrado por outro usuário."
            )
            
    updated_user = crud_usuario.update_usuario(db=db, db_user=db_user, user_update=usuario_in)
    return updated_user

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(
    usuario_id: int, 
    db: Session = Depends(get_db)
    # current_user: models.Usuario = Depends(get_simulated_current_user) # Exemplo de proteção
):
    # Lógica de permissão (exemplo):
    # if usuario_id != current_user.id and not current_user.is_admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a deletar este usuário")

    deleted_user = crud_usuario.delete_usuario(db, usuario_id=usuario_id)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado para deletar")
    return

