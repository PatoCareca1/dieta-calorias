# src/api/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importar modelos e CRUD se get_simulated_current_user precisar deles diretamente aqui
from src import models
from src.crud import usuario as crud_usuario

# Importar SessionLocal do seu arquivo de banco de dados
from src.database import SessionLocal

# ---- FUNÇÃO get_db CORRIGIDA ----
def get_db():
    """
    Dependência para fornecer uma sessão de banco de dados SQLAlchemy
    e garantir que ela seja fechada após a requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- FUNÇÃO DE DEPENDÊNCIA SIMULADA (get_simulated_current_user) ----
async def get_simulated_current_user(db: Session = Depends(get_db)) -> models.Usuario:
    """
    Simula um usuário autenticado pegando um usuário fixo do banco (ex: ID 1).
    Em uma aplicação real, isso seria substituído por lógica de token OAuth2.
    """
    user_id_simulado = 1 
    user = crud_usuario.get_usuario(db, usuario_id=user_id_simulado)
    if user is None:
        # Se o usuário simulado não existir, podemos criar um para teste ou levantar um erro mais específico.
        # Por enquanto, vamos manter o erro 401 para indicar que a "autenticação" falhou.
        # Ou você pode preferir um 500 aqui para indicar um problema de setup de teste.
        # Alternativamente, crie o usuário com ID 1 no seu banco de dados antes de testar.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Usuário simulado com ID {user_id_simulado} não encontrado. Crie este usuário para teste.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
