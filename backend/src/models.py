import enum
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, Date, Float, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# --- ENUMS ---

class GeneroEnum(str, enum.Enum):
    masculino = "masculino"
    feminino = "feminino"
    outro = "outro"
    prefiro_nao_dizer = "prefiro_nao_dizer"

class NivelAtividadeEnum(str, enum.Enum):
    sedentario = "sedentario"
    levemente_ativo = "levemente_ativo"
    moderadamente_ativo = "moderadamente_ativo"
    muito_ativo = "muito_ativo"
    extremamente_ativo = "extremamente_ativo"

class ObjetivoEnum(str, enum.Enum):
    perder_peso = "perder_peso"
    manter_peso = "manter_peso"
    ganhar_massa = "ganhar_massa"

class GrupoMuscularEnum(str, enum.Enum):
    PEITO = "Peito"
    COSTAS = "Costas"
    PERNAS = "Pernas"
    BICEPS = "Bíceps"
    TRICEPS = "Tríceps"
    OMBROS = "Ombros"
    ABDOMEN = "Abdômen"
    OUTRO = "Outro"


# --- MODELOS DA APLICAÇÃO ---

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default=sa.text('true'))
    peso_kg = Column(Float, nullable=True)
    altura_cm = Column(Integer, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    genero = Column(SQLAlchemyEnum(GeneroEnum, name="generoenum"), nullable=True)
    nivel_atividade = Column(SQLAlchemyEnum(NivelAtividadeEnum, name="nivelatividadeenum"), nullable=True)
    objetivo = Column(SQLAlchemyEnum(ObjetivoEnum, name="objetivoenum"), nullable=True)
    restricoes_alimentares = Column(String, nullable=True)
    observacoes = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Relacionamentos
    plano_alimentar = relationship("PlanoAlimentar", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    refeicoes = relationship("Refeicao", back_populates="usuario", cascade="all, delete-orphan")
    treinos = relationship("Treino", back_populates="usuario", cascade="all, delete-orphan")


class PlanoAlimentar(Base):
    __tablename__ = "planos_alimentares"
    id = Column(Integer, primary_key=True, index=True)
    
    tmb = Column(Float, nullable=False)
    calorias_objetivo = Column(Float, nullable=False)
    proteinas_g = Column(Float, nullable=False)
    carboidratos_g = Column(Float, nullable=False)
    gorduras_g = Column(Float, nullable=False)
    data_criacao = Column(Date, default=sa.func.current_date(), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False, index=True)
    usuario = relationship("Usuario", back_populates="plano_alimentar")

# --- Modelos para DIETA ---

class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    marca = Column(String, nullable=True)
    # Padronizando para 100g para facilitar cálculos
    calorias_por_100g = Column(Float, nullable=False)
    proteinas_por_100g = Column(Float, nullable=True)
    carboidratos_por_100g = Column(Float, nullable=True)
    gorduras_por_100g = Column(Float, nullable=True)
    
    itens = relationship("ItemRefeicao", back_populates="alimento")

class Refeicao(Base):
    __tablename__ = "refeicoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False) # Ex: Café da Manhã
    horario = Column(String, nullable=True) # Ex: 08:00
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="refeicoes")
    itens = relationship("ItemRefeicao", back_populates="refeicao", cascade="all, delete-orphan")

class ItemRefeicao(Base):
    __tablename__ = "itens_refeicao"

    id = Column(Integer, primary_key=True, index=True)
    refeicao_id = Column(Integer, ForeignKey("refeicoes.id"), nullable=False)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=False)
    quantidade_gramas = Column(Float, nullable=False) # Campo mais descritivo

    refeicao = relationship("Refeicao", back_populates="itens")
    alimento = relationship("Alimento", back_populates="itens")

# --- Modelos para TREINO ---

class Exercicio(Base):
    __tablename__ = 'exercicios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, unique=True, nullable=False)
    grupo_muscular = Column(SQLAlchemyEnum(GrupoMuscularEnum, name="grupomuscularenum"), nullable=False)
    descricao = Column(String, nullable=True)
    
    # Relacionamento com a tabela associativa
    itens_treino = relationship("ItemTreino", back_populates="exercicio")

class Treino(Base):
    __tablename__ = 'treinos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False) # Ex: Treino A - Foco em Peito
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="treinos")
    itens = relationship("ItemTreino", back_populates="treino", cascade="all, delete-orphan")

class ItemTreino(Base):
    __tablename__ = 'itens_treino'
    
    id = Column(Integer, primary_key=True, index=True)
    treino_id = Column(Integer, ForeignKey('treinos.id'), nullable=False)
    exercicio_id = Column(Integer, ForeignKey('exercicios.id'), nullable=False)
    
    # Detalhes do exercício no treino
    series = Column(Integer, nullable=True)
    repeticoes = Column(String, nullable=True) # String para "8-12" ou "Até a falha"
    descanso_segundos = Column(Integer, nullable=True)
    
    treino = relationship("Treino", back_populates="itens")
    exercicio = relationship("Exercicio", back_populates="itens_treino")