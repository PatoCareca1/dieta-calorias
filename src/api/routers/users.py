from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.crud.usuario import create_user, get_user_by_email, update_user, delete_user
from src.api.schemas import UsuarioCreate, UsuarioRead
from src.models import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def api_create_user(data: UsuarioCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return create_user(db, **data.dict())

@router.get("/{user_id}", response_model=UsuarioRead)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/{user_id}", response_model=UsuarioRead)
def api_update_user(user_id: int, data: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return update_user(db, usuario, **data.dict())

# >>> NOVO: DELETE /usuarios/{user_id}
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    delete_user(db, usuario)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
