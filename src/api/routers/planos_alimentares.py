from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import models
from src.api import schemas
from src.api.dependencies import get_db
from src.api.security import get_current_active_user
from src.services import diet_calculator
from src.crud import plano_alimentar as crud_plano_alimentar

router = APIRouter(
    prefix="/planos-alimentares",
    tags=["Planos Alimentares"],
    responses={404: {"description": "Não encontrado"}},
)

@router.post("/me/calcular", response_model=schemas.PlanoAlimentarRead)
def api_calcular_e_salvar_plano_pessoal(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """
    Calcula (ou recalcula) e salva o plano alimentar para o usuário autenticado.

    Este endpoint usa os dados do perfil do usuário (peso, altura, objetivo, etc.)
    para calcular as necessidades calóricas e de macronutrientes.
    O resultado é salvo no banco de dados, substituindo qualquer plano anterior.
    """
    try:
        # 1. Chamar o serviço de cálculo
        dados_calculados = diet_calculator.calcular_plano_alimentar(user=current_user)
        
        # 2. Criar um objeto schema Pydantic com os resultados
        plano_para_db = schemas.PlanoAlimentarCreate(**dados_calculados)

        # 3. Usar o CRUD para salvar (ou atualizar) no banco
        plano_salvo = crud_plano_alimentar.create_or_update_plano_alimentar(
            db=db,
            plano_in=plano_para_db,
            usuario_id=current_user.id
        )
        return plano_salvo

    except ValueError as e:
        # Erro levantado pelo diet_calculator se os dados do perfil estiverem incompletos
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não foi possível calcular o plano: {e}"
        )
    except Exception as e:
        # Captura outros erros inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado: {e}"
        )
