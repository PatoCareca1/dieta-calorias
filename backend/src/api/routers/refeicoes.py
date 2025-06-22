from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud.refeicao import (
    create_refeicao, get_refeicao_by_id,
    update_refeicao, delete_refeicao
)
from src.api.dependencies import get_db
from src.api.schemas import RefeicaoCreate, RefeicaoRead
from src.models import Usuario

router = APIRouter(prefix="/refeicoes", tags=["Refeições"])

@router.post("/", response_model=RefeicaoRead, status_code=status.HTTP_201_CREATED)
def api_create_refeicao(data: RefeicaoCreate, db: Session = Depends(get_db)):
    user = db.query(Usuario).get(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    ref = create_refeicao(db,
                         usuario=user,
                         data=data.data,
                         tipo_refeicao=data.tipo_refeicao)
    return ref

@router.get("/{id_refeicao}", response_model=RefeicaoRead)
def api_get_refeicao(id_refeicao: int, db: Session = Depends(get_db)):
    ref = get_refeicao_by_id(db, id_refeicao)
    if not ref:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return ref

@router.put("/{id_refeicao}", response_model=RefeicaoRead)
def api_update_refeicao(id_refeicao: int, data: RefeicaoCreate, db: Session = Depends(get_db)):
    ref = get_refeicao_by_id(db, id_refeicao)
    if not ref:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    updated = update_refeicao(db,
                              refeicao=ref,
                              data=data.data,
                              tipo_refeicao=data.tipo_refeicao)
    return updated

@router.delete("/{id_refeicao}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_refeicao(id_refeicao: int, db: Session = Depends(get_db)):
    ref = get_refeicao_by_id(db, id_refeicao)
    if not ref:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    delete_refeicao(db, ref)
