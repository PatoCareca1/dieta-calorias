import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, Float, Enum as SQLAlchemyEnum, ForeignKey # Adicionado Date, Float, SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .database import Base

# Definições dos Enums
class GeneroEnum(enum.Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"
    PREFIRO_NAO_DIZER = "prefiro_nao_dizer"

class NivelAtividadeEnum(enum.Enum):
    SEDENTARIO = "sedentario"
    LEVEMENTE_ATIVO = "levemente_ativo"
    MODERADAMENTE_ATIVO = "moderadamente_ativo"
    MUITO_ATIVO = "muito_ativo"
    EXTREMAMENTE_ATIVO = "extremamente_ativo"

class ObjetivoEnum(enum.Enum):
    PERDER_PESO = "perder_peso"
    MANTER_PESO = "manter_peso"
    GANHAR_MASSA = "ganhar_massa"

class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    marca = Column(String, nullable=True)
    porcao_gramas = Column(Float, nullable=False)
    calorias_por_porcao = Column(Float, nullable=False)
    carboidratos_g = Column(Float, nullable=True)
    proteinas_g = Column(Float, nullable=True)
    gorduras_g = Column(Float, nullable=True)
    # usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True) 
    
    itens_refeicao = relationship("ItemRefeicao", back_populates="alimento")

class Refeicao(Base):
    __tablename__ = "refeicoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False) # Ex: Café da manhã, Almoço, Jantar
    horario = Column(String, nullable=True) # Poderia ser Time, mas String é mais flexível para "Manhã", "Tarde"
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="refeicoes")
    itens_refeicao = relationship("ItemRefeicao", back_populates="refeicao", cascade="all, delete-orphan")


class ItemRefeicao(Base):
    __tablename__ = "itens_refeicao"

    id = Column(Integer, primary_key=True, index=True)
    refeicao_id = Column(Integer, ForeignKey("refeicoes.id"), nullable=False)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=False)
    quantidade = Column(Float, nullable=False) # Quantidade do alimento (ex: 2.0 unidades da porção, ou 200g se porção_gramas=100g)

    refeicao = relationship("Refeicao", back_populates="itens_refeicao")
    alimento = relationship("Alimento", back_populates="itens_refeicao")


# Modelo Usuario modificado
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=True) # Decida se nome pode ser nulo
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # --- NOVOS CAMPOS DO PERFIL ---
    peso_kg = Column(Float, nullable=True)
    altura_cm = Column(Integer, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    
    genero = Column(SQLAlchemyEnum(GeneroEnum), nullable=True)
    nivel_atividade = Column(SQLAlchemyEnum(NivelAtividadeEnum), nullable=True)
    objetivo = Column(SQLAlchemyEnum(ObjetivoEnum), nullable=True)
    
    restricoes_alimentares = Column(String, nullable=True)
    observacoes = Column(String, nullable=True)

    refeicoes = relationship("Refeicao", back_populates="usuario")