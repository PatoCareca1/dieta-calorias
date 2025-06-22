from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud.item_refeicao import (
    create_item_refeicao,
    get_item_refeicao_by_id,
    update_item_refeicao,
    delete_item_refeicao
)
from src.api.dependencies import get_db
from src.api.schemas import ItemRefeicaoCreate, ItemRefeicaoRead
from src.models import Refeicao, Alimento

router = APIRouter(prefix="/itens-refeicao", tags=["ItensRefeição"])

@router.post("/", response_model=ItemRefeicaoRead, status_code=status.HTTP_201_CREATED)
def api_create_item(data: ItemRefeicaoCreate, db: Session = Depends(get_db)):
    ref = db.get(Refeicao, data.id_refeicao)
    if not ref:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    alim = db.get(Alimento, data.id_alimento)
    if not alim:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    item = create_item_refeicao(
        db,
        refeicao=ref,
        alimento=alim,
        quantidade_em_gramas=data.quantidade_em_gramas
    )
    return item

@router.get("/{id_item}", response_model=ItemRefeicaoRead)
def api_get_item(id_item: int, db: Session = Depends(get_db)):
    item = get_item_refeicao_by_id(db, id_item)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.put("/{id_item}", response_model=ItemRefeicaoRead)
def api_update_item(id_item: int, data: ItemRefeicaoCreate, db: Session = Depends(get_db)):
    item = get_item_refeicao_by_id(db, id_item)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    # opcional: validar se id_refeicao/id_alimento existem
    return update_item_refeicao(db, item, **data.dict())

@router.delete("/{id_item}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_item(id_item: int, db: Session = Depends(get_db)):
    item = get_item_refeicao_by_id(db, id_item)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    delete_item_refeicao(db, item)
