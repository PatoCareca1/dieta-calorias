# src/main.py
import uvicorn
from fastapi import FastAPI
# Base e engine
from src.api.routers import users, calorias, alimentos, refeicoes, itens_refeicao
import src.database as database
from src.database import Base

app = FastAPI(title="API Dieta-Calorias", version="0.1.0")

# routers
app.include_router(users.router)
app.include_router(calorias.router)
app.include_router(alimentos.router)
app.include_router(refeicoes.router)
app.include_router(itens_refeicao.router)


@app.on_event("startup")
def on_startup():
    # cria todas as tabelas no engine atual em database.engine
    Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
