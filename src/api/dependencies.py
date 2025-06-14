# src/api/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import models
from src.crud import usuario as crud_usuario

# Importar SessionLocal do seu arquivo de banco de dados
from src.database import SessionLocal

# ---- FUNÇÃO get_db ----
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

# A dependência de autenticação (get_current_active_user) será adicionada em
# um passo futuro, após esta migração funcionar.