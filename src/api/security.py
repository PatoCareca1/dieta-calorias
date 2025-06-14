from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Importar dependências e CRUD
from src.api.dependencies import get_db
from src.crud import usuario as crud_usuario
from src.api import schemas
from src import models

# Carregar variáveis de ambiente
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configuração de Segurança ---
SECRET_KEY = os.getenv("SECRET_KEY", "uma_chave_secreta_padrao_se_nao_definida")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme - aponta para o endpoint de login que criamos
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Cria um novo token de acesso JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependência de Autenticação Real ---
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> models.Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud_usuario.get_usuario_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: models.Usuario = Depends(get_current_user)
) -> models.Usuario:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

async def get_current_admin_user(
    current_user: models.Usuario = Depends(get_current_active_user)
) -> models.Usuario:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="O usuário não tem privilégios de administrador"
        )
    return current_user
