from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List
from src.models import GeneroEnum, NivelAtividadeEnum, ObjetivoEnum 

# ----- Schemas de Alimento -----
class AlimentoBase(BaseModel):
    nome: str
    calorias_por_porcao: float 
    porcao_gramas: float = Field(default=100.0)
    proteinas: Optional[float] = Field(None, alias="proteinas_g")
    carboidratos: Optional[float] = Field(None, alias="carboidratos_g")
    gorduras: Optional[float] = Field(None, alias="gorduras_g")
    marca: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class AlimentoCreate(AlimentoBase):
    pass

class AlimentoRead(AlimentoBase):
    id: int

# ----- Schemas de ItemRefeicao -----
class ItemRefeicaoBase(BaseModel):
    alimento_id: int
    quantidade: float

class ItemRefeicaoCreate(ItemRefeicaoBase):
    pass

class ItemRefeicaoRead(ItemRefeicaoBase):
    id: int
    alimento: Optional[AlimentoRead] = None 

    class Config:
        from_attributes = True

# ----- Schemas de Refeição -----
class RefeicaoBase(BaseModel):
    nome: str
    data: date
    horario: Optional[str] = None

class RefeicaoCreate(RefeicaoBase):
    pass

class RefeicaoRead(RefeicaoBase):
    id: int
    usuario_id: int
    itens_refeicao: List[ItemRefeicaoRead] = []

    class Config:
        from_attributes = True

# ----- Schemas para PlanoAlimentar -----
class PlanoAlimentarBase(BaseModel):
    tmb: float # Taxa metabolica basal
    calorias_objetivo: float
    proteinas_g: float
    carboidratos_g: float
    gorduras_g: float

class PlanoAlimentarCreate(PlanoAlimentarBase):
    pass 

class PlanoAlimentarRead(PlanoAlimentarBase):
    id: int
    usuario_id: int
    data_criacao: date

    class Config:
        from_attributes = True
        
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
    is_admin : Optional[bool] = False

    class Config:
        from_attributes = True
        use_enum_values = True 

class UsuarioCreate(UsuarioBase):
    nome: str 
    email: EmailStr
    senha: str = Field(..., min_length=8)
    is_admin : bool = False

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
        from_attributes = True
        use_enum_values = True


class UsuarioRead(UsuarioBase):
    id: int
    refeicoes: List[RefeicaoRead] = []
    plano_alimentar: Optional[PlanoAlimentarRead] = None


# ----- Outros Schemas -----
class ResumoDiario(BaseModel):
    data: date
    total_calorias: float
    status: str = Field(..., example="dentro")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

