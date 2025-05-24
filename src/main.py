# src/main.py
import uvicorn
from fastapi import FastAPI

import src.database as database
from src.api.routers import users, calorias, alimentos, refeicoes, itens_refeicao

# **Garante que as tabelas existem assim que o módulo é carregado**
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API Dieta-Calorias", version="0.1.0")

# Routers
app.include_router(users.router)
app.include_router(calorias.router)
app.include_router(alimentos.router)
app.include_router(refeicoes.router)
app.include_router(itens_refeicao.router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
