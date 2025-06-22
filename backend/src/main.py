from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import users, calorias, alimentos, refeicoes, itens_refeicao, planos_alimentares, auth

app = FastAPI(
    title="API de Dieta e Calorias",
    description="Uma API para ajudar no gerenciamento de dietas e contagem de calorias.",
    version="0.1.0",
)

origins = [
    "http://localhost:5173", 
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,      
    allow_methods=["*"],         
    allow_headers=["*"],         
)

app.include_router(auth.router)   
app.include_router(users.router)
app.include_router(alimentos.router)
app.include_router(refeicoes.router)
app.include_router(itens_refeicao.router)
app.include_router(calorias.router)
app.include_router(planos_alimentares.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz da API.
    """
    return {"message": "Bem-vindo à API de Dieta e Calorias!"}