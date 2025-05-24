from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from src.api.dependencies import get_db
from src.api.schemas import ResumoDiario
from src.services.calculadora_calorias import (
    calcular_calorias_por_dia, avaliar_consumo_diario
)
from src.models import Usuario

router = APIRouter(prefix="/calorias", tags=["Calorias"])

@router.get("/resumo/{user_id}", response_model=ResumoDiario)
def api_resumo_diario(user_id: int, dia: date = date.today(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).get(user_id)
    if not usuario:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    total = calcular_calorias_por_dia(db, usuario, dia)
    status = avaliar_consumo_diario(usuario, total)
    return ResumoDiario(data=dia, total_calorias=total, status=status)
