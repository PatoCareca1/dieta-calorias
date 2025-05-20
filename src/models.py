from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    meta_calorica_diaria = Column(Integer, nullable=False)

    refeicoes = relationship("Refeicao", back_populates="usuario")

class Alimento(Base):
    __tablename__ = 'alimentos'
    id_alimento = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    calorias_por_100g = Column(Float, nullable=False)
    proteinas = Column(Float, nullable=False)
    carboidratos = Column(Float, nullable=False)
    gorduras = Column(Float, nullable=False)

    itens_refeicao = relationship("ItemRefeicao", back_populates="alimento")

class Refeicao(Base):
    __tablename__ = 'refeicoes'
    id_refeicao = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    data = Column(Date, nullable=False)
    tipo_refeicao = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="refeicoes")
    itens_refeicao = relationship("ItemRefeicao", back_populates="refeicao")

class ItemRefeicao(Base):
    __tablename__ = 'itens_refeicao'
    id_item = Column(Integer, primary_key=True)
    id_refeicao = Column(Integer, ForeignKey("refeicoes.id_refeicao"))
    id_alimento = Column(Integer, ForeignKey("alimentos.id_alimento"))
    quantidade_em_gramas = Column(Float, nullable=False)

    refeicao = relationship("Refeicao", back_populates="itens_refeicao")
    alimento = relationship("Alimento", back_populates="itens_refeicao")
