from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List

# Importar Enums dos seus modelos SQLAlchemy
from src.models import GeneroEnum, NivelAtividadeEnum, ObjetivoEnum 

# ----- Schemas de Alimento (Definidos primeiro para clareza) -----
class AlimentoBase(BaseModel):
    nome: str
    calorias_por_porcao: float 
    porcao_gramas: float = Field(default=100.0) # No seu modelo é porcao_gramas
    proteinas: Optional[float] = Field(None, alias="proteinas_g") # Alias para corresponder ao modelo
    carboidratos: Optional[float] = Field(None, alias="carboidratos_g") # Alias para corresponder ao modelo
    gorduras: Optional[float] = Field(None, alias="gorduras_g") # Alias para corresponder ao modelo
    marca: Optional[str] = None

    class Config:
        from_attributes = True # ATUALIZADO de orm_mode
        populate_by_name = True # Permite usar 'proteinas_g' ao criar a partir do modelo ORM

class AlimentoCreate(AlimentoBase):
    pass # Herda todos os campos de AlimentoBase

class AlimentoRead(AlimentoBase):
    id: int

# ----- Schemas de ItemRefeicao -----
class ItemRefeicaoBase(BaseModel):
    alimento_id: int
    quantidade: float # Corresponde a 'quantidade' no seu modelo ItemRefeicao

class ItemRefeicaoCreate(ItemRefeicaoBase):
    # id_refeicao será provavelmente passado no path ou gerenciado pelo endpoint
    pass

class ItemRefeicaoRead(ItemRefeicaoBase):
    id: int
    # Se quiser mostrar detalhes do alimento aqui, o AlimentoRead já está definido
    alimento: Optional[AlimentoRead] = None 

    class Config:
        from_attributes = True # ATUALIZADO

# ----- Schemas de Refeição -----
class RefeicaoBase(BaseModel):
    nome: str # Nome principal da refeição (ex: "Café da Manhã da Semana")
    data: date
    horario: Optional[str] = None # Ex: "08:00", "Manhã"

class RefeicaoCreate(RefeicaoBase):
    # usuario_id será adicionado no CRUD, vindo do usuário autenticado
    pass

class RefeicaoRead(RefeicaoBase):
    id: int
    usuario_id: int
    itens_refeicao: List[ItemRefeicaoRead] = []

    class Config:
        from_attributes = True # ATUALIZADO

# ----- Schemas de Usuário -----
class UsuarioBase(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    
    peso_kg: Optional[float] = Field(None, gt=0, description="Peso em quilogramas")
    altura_cm: Optional[int] = Field(None, gt=0, description="Altura em centímetros")
    data_nascimento: Optional[date] = None
    genero: Optional[GeneroEnum] = None
    nivel_atividade: Optional[NivelAtividadeEnum] = None
    objetivo: Optional[ObjetivoEnum] = None
    restricoes_alimentares: Optional[str] = None
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True # ATUALIZADO
        use_enum_values = True 


class UsuarioCreate(UsuarioBase):
    nome: str 
    email: EmailStr
    senha: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel): 
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    
    peso_kg: Optional[float] = Field(None, gt=0, description="Peso em quilogramas")
    altura_cm: Optional[int] = Field(None, gt=0, description="Altura em centímetros")
    data_nascimento: Optional[date] = None
    genero: Optional[GeneroEnum] = None
    nivel_atividade: Optional[NivelAtividadeEnum] = None
    objetivo: Optional[ObjetivoEnum] = None
    restricoes_alimentares: Optional[str] = None
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True # ATUALIZADO
        use_enum_values = True


class UsuarioRead(UsuarioBase):
    id: int
    refeicoes: List[RefeicaoRead] = []

    # A senha não é retornada

# ----- Outros Schemas -----
class ResumoDiario(BaseModel): # Supondo que este não precise de from_attributes se não mapear de ORM
    data: date
    total_calorias: float
    status: str = Field(..., example="dentro")

