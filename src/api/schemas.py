from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

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

# ----- Alimento -----

class AlimentoCreate(BaseModel):
    nome: str
    calorias_por_100g: float
    proteinas: float
    carboidratos: float
    gorduras: float

class AlimentoRead(AlimentoCreate):
    id_alimento: int

    class Config:
        orm_mode = True

# ----- Refeição -----
class RefeicaoCreate(BaseModel):
    user_id: int
    data: date
    tipo_refeicao: str

class RefeicaoRead(BaseModel):
    id_refeicao: int
    id_usuario: int
    data: date
    tipo_refeicao: str

    class Config:
        orm_mode = True

# ----- ItemRefeição -----
class ItemRefeicaoCreate(BaseModel):
    id_refeicao: int
    id_alimento: int
    quantidade_em_gramas: float

class ItemRefeicaoRead(ItemRefeicaoCreate):
    id_item: int

    class Config:
        orm_mode = True