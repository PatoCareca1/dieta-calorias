from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud.usuario import (
    create_user, get_user_by_email
)
from src.api.dependencies import get_db
from src.api.schemas import UsuarioCreate, UsuarioRead

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def api_create_user(data: UsuarioCreate, db: Session = Depends(get_db)):
    # evita duplicidade de email:
    if get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    usuario = create_user(db, **data.dict())
    return usuario

@router.get("/{user_id}", response_model=UsuarioRead)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(__import__("src.models").models.Usuario).get(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario
