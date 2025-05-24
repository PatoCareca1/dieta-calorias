from pydantic import BaseModel, EmailStr, Field

# ----- Usuário -----
class UsuarioCreate(BaseModel):
    nome: str = Field(..., example="Ana Silva")
    email: EmailStr
    senha: str = Field(..., min_length=6)
    peso: float
    altura: float
    meta_calorica_diaria: int

class UsuarioRead(BaseModel):
    id_usuario: int
    nome: str
    email: EmailStr
    peso: float
    altura: float
    meta_calorica_diaria: int

    class Config:
        orm_mode = True

# ----- Calorias (exemplo de endpoint de resumo diário) -----
from datetime import date

class ResumoDiario(BaseModel):
    data: date
    total_calorias: float
    status: str = Field(..., example="dentro")
