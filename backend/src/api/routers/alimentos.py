from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud.alimento import (
    create_alimento, get_alimento_by_nome,
    update_alimento, delete_alimento
)
from src.api.dependencies import get_db
from src.api.schemas import AlimentoCreate, AlimentoRead

router = APIRouter(prefix="/alimentos", tags=["Alimentos"])

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED)
def api_create_alimento(data: AlimentoCreate, db: Session = Depends(get_db)):
    if get_alimento_by_nome(db, data.nome):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alimento já cadastrado"
        )
    return create_alimento(db, **data.dict())

@router.get("/{id_alimento}", response_model=AlimentoRead)
def api_get_alimento(id_alimento: int, db: Session = Depends(get_db)):
    alim = db.query(__import__("src.models").models.Alimento).get(id_alimento)
    if not alim:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return alim

@router.put("/{id_alimento}", response_model=AlimentoRead)
def api_update_alimento(
    id_alimento: int,
    data: AlimentoCreate,
    db: Session = Depends(get_db)
):
    alim = db.query(__import__("src.models").models.Alimento).get(id_alimento)
    if not alim:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return update_alimento(db, alim, **data.dict())

@router.delete("/{id_alimento}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_alimento(id_alimento: int, db: Session = Depends(get_db)):
    alim = db.query(__import__("src.models").models.Alimento).get(id_alimento)
    if not alim:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    delete_alimento(db, alim)
