# src/api/routers/users.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.models import Usuario
from src.api.schemas import UsuarioCreate, UsuarioRead, UsuarioUpdate
from src.crud.usuario import create_user, get_user_by_email, update_user, delete_user
from src.api.dependencies import get_db    # ← ajuste aqui

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def api_create_user(data: UsuarioCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return create_user(db, **data.model_dump())

@router.get("/{user_id}", response_model=UsuarioRead)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/{user_id}", response_model=UsuarioRead)
def api_update_user(
    user_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    usuario = db.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return update_user(db, usuario, **data.model_dump())

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    delete_user(db, usuario)  # passando a instância
    return
