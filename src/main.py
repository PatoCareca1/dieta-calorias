import uvicorn
from fastapi import FastAPI
from src.api.routers import users, calorias  # importa os routers

app = FastAPI(title="API Dieta-Calorias", version="0.1.0")

# inclui routers
app.include_router(users.router)
app.include_router(calorias.router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
