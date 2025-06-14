# src/api/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from src.api.dependencies import get_db
from src.crud.usuario import authenticate_user
from src.api.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.api.schemas import Token

router = APIRouter(tags=["Autenticação"])

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Endpoint de login. Recebe e-mail (no campo 'username') e senha.
    Retorna um token de acesso JWT se as credenciais forem válidas.
    """
    # O campo 'username' do formulário OAuth2 é usado para o e-mail aqui
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

