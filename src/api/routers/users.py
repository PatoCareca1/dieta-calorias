from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src import models
from src.api import schemas
from src.crud import usuario as crud_usuario 
from src.api.dependencies import get_db
from src.api.security import get_current_active_user, get_current_admin_user

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
    """
    Cria um novo usuário, incluindo os campos de perfil.
    Este endpoint é público.
    """
    db_user_by_email = crud_usuario.get_usuario_by_email(db, email=usuario_in.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está registrado."
        )
    # No schema de criação, vamos garantir que um usuário não pode se criar como admin
    usuario_in.is_admin = False # Força que novos usuários não sejam administradores
    created_user = crud_usuario.create_usuario(db=db, usuario=usuario_in)
    return created_user

@router.get("/", response_model=List[schemas.UsuarioRead])
def api_get_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    # Protege o endpoint: apenas administradores podem listar todos os usuários
    current_admin: models.Usuario = Depends(get_current_admin_user)
):
    """
    (Admin) Lista todos os usuários cadastrados com paginação.
    """
    usuarios = crud_usuario.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/me/", response_model=schemas.UsuarioRead)
def api_get_current_user_me(
    # Protege o endpoint: requer um usuário ativo e logado
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Obtém os dados do perfil do usuário autenticado.
    """
    return current_user

@router.get("/{usuario_id}", response_model=schemas.UsuarioRead)
def api_get_user(
    usuario_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user) # Protegido
):
    """
    Obtém os detalhes de um usuário específico pelo ID.
    Um admin pode ver qualquer usuário. Um usuário normal só pode ver a si mesmo.
    """
    if usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Não autorizado a acessar este recurso"
        )

    db_user = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return db_user

@router.put("/me/", response_model=schemas.UsuarioRead)
def api_update_current_user_me(
    usuario_in: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Atualiza o perfil do próprio usuário autenticado.
    """
    # Verifica se o e-mail está sendo atualizado para um que já existe por outro usuário
    if usuario_in.email and usuario_in.email != current_user.email:
        existing_user_by_email = crud_usuario.get_usuario_by_email(db, email=usuario_in.email)
        if existing_user_by_email and existing_user_by_email.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail já está registrado por outro usuário."
            )

    updated_user = crud_usuario.update_usuario(db=db, db_user=current_user, user_update=usuario_in)
    return updated_user


# Endpoint para um admin atualizar qualquer usuário.
@router.put("/{usuario_id}", response_model=schemas.UsuarioRead)
def api_update_user_by_admin(
    usuario_id: int,
    usuario_in: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Usuario = Depends(get_current_admin_user)
):
    """
    (Admin) Atualiza o perfil de um usuário específico.
    """
    db_user = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    updated_user = crud_usuario.update_usuario(db=db, db_user=db_user, user_update=usuario_in)
    return updated_user


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(
    usuario_id: int, 
    db: Session = Depends(get_db),
    current_admin: models.Usuario = Depends(get_current_admin_user) # Apenas admin pode deletar
):
    """
    (Admin) Deleta um usuário.
    """
    deleted_user = crud_usuario.delete_usuario(db, usuario_id=usuario_id)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado para deletar")
    return

