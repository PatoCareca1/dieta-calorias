# src/main.py
import uvicorn
from fastapi import FastAPI
# Base e engine
from src.database import Base, engine  
from src.api.routers import users, calorias, alimentos

app = FastAPI(title="API Dieta-Calorias", version="0.1.0")

# routers
app.include_router(users.router)
app.include_router(calorias.router)
app.include_router(alimentos.router)

@app.on_event("startup")
def on_startup():
    """
    Cria (se não existirem) todas as tabelas do nosso ORM
    sempre que a aplicação iniciar.
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
