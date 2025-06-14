import enum
import sqlalchemy as sa 
from sqlalchemy import Column, Integer, String, Boolean, Date, Float, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class GeneroEnum(enum.Enum):
    masculino = "masculino"
    feminino = "feminino"
    outro = "outro"
    prefiro_nao_dizer = "prefiro_nao_dizer"

class NivelAtividadeEnum(enum.Enum):
    sedentario = "sedentario"
    levemente_ativo = "levemente_ativo"
    moderadamente_ativo = "moderadamente_ativo"
    muito_ativo = "muito_ativo"
    extremamente_ativo = "extremamente_ativo"

class ObjetivoEnum(enum.Enum):
    perder_peso = "perder_peso"
    manter_peso = "manter_peso"
    ganhar_massa = "ganhar_massa"

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
    
    itens_refeicao = relationship("ItemRefeicao", back_populates="alimento")

class Refeicao(Base):
    __tablename__ = "refeicoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    horario = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="refeicoes")
    itens_refeicao = relationship("ItemRefeicao", back_populates="refeicao", cascade="all, delete-orphan")


class ItemRefeicao(Base):
    __tablename__ = "itens_refeicao"

    id = Column(Integer, primary_key=True, index=True)
    refeicao_id = Column(Integer, ForeignKey("refeicoes.id"), nullable=False)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=False)
    quantidade = Column(Float, nullable=False)

    refeicao = relationship("Refeicao", back_populates="itens_refeicao")
    alimento = relationship("Alimento", back_populates="itens_refeicao")

class PlanoAlimentar(Base):
    __tablename__ = "planos_alimentares"
    id = Column(Integer, primary_key=True, index=True)
    
    # Campos calculados da dieta
    tmb = Column(Float, nullable=False)
    calorias_objetivo = Column(Float, nullable=False)
    proteinas_g = Column(Float, nullable=False)
    carboidratos_g = Column(Float, nullable=False)
    gorduras_g = Column(Float, nullable=False)
    data_criacao = Column(Date, default=sa.func.current_date(), nullable=False)

    # Relacionamento com o usuário
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False, index=True)
    usuario = relationship("Usuario", back_populates="plano_alimentar")
    
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default=sa.text('true')) # 'sa' agora está definido
    peso_kg = Column(Float, nullable=True)
    altura_cm = Column(Integer, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    genero = Column(SQLAlchemyEnum(GeneroEnum, name="generoenum", native_enum=True, create_constraint=True), nullable=True) 
    nivel_atividade = Column(SQLAlchemyEnum(NivelAtividadeEnum, name="nivelatividadeenum", native_enum=True, create_constraint=True), nullable=True)
    objetivo = Column(SQLAlchemyEnum(ObjetivoEnum, name="objetivoenum", native_enum=True, create_constraint=True), nullable=True)
    restricoes_alimentares = Column(String, nullable=True)
    observacoes = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    refeicoes = relationship("Refeicao", back_populates="usuario")
    plano_alimentar = relationship("PlanoAlimentar", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

