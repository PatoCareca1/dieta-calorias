# src/api/routers/planos_alimentares.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src import models
from src.api import schemas
from src.api.dependencies import get_db
# 1. Importando as duas funções de segurança necessárias do local correto
from src.api.security import get_current_active_user, get_current_admin_user
from src.services import diet_calculator
from src.crud import plano_alimentar as crud_plano_alimentar

router = APIRouter(
    prefix="/planos-alimentares",
    tags=["Planos Alimentares"],
    responses={404: {"description": "Não encontrado"}},
)

# 2. ENDPOINT ADICIONADO para o administrador visualizar todos os planos
@router.get("/", response_model=List[schemas.PlanoAlimentarRead])
def read_planos_alimentares(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: models.Usuario = Depends(get_current_admin_user)
):
    """
    (Admin) Retorna uma lista de todos os planos alimentares de todos os usuários.
    """
    planos = crud_plano_alimentar.get_planos_alimentares(db, skip=skip, limit=limit)
    return planos


@router.post("/me/calcular", response_model=schemas.PlanoAlimentarRead)
def api_calcular_e_salvar_plano_pessoal(
    db: Session = Depends(get_db),
    # A dependência aqui já estava correta, apenas a importação precisava ser garantida
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Calcula (ou recalcula) e salva o plano alimentar para o usuário autenticado.
    """
    try:
        dados_calculados = diet_calculator.calcular_plano_alimentar(user=current_user)
        
        plano_para_db = schemas.PlanoAlimentarCreate(**dados_calculados)

        plano_salvo = crud_plano_alimentar.create_or_update_plano_alimentar(
            db=db,
            plano_in=plano_para_db,
            usuario_id=current_user.id
        )
        return plano_salvo

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não foi possível calcular o plano: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado: {e}"
        )