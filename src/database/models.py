from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Tipi(Base):
    __tablename__ = "tipi"

    id_tipi = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(100), nullable=False)
    aliquota = Column(Numeric(5, 2), nullable=False)
    ncm = Column(String(8), nullable=False)

    produtos = relationship("Produto", back_populates="tipi")


class Produto(Base):
    __tablename__ = "produto"

    part_number = Column(String(25), primary_key=True, index=True)
    nome = Column(String(100))
    fornecedor = Column(String(100))
    pais_origem = Column(String(2))
    id_tipi = Column(Integer, ForeignKey("tipi.id_tipi"))

    tipi = relationship("Tipi", back_populates="produtos")
    historicos = relationship("Historico", back_populates="produto")


class Historico(Base):
    __tablename__ = "historico"

    id_historico = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hash_code = Column(String(256), nullable=False)
    process_data = Column(DateTime, default=datetime.now)
    part_number = Column(String(25), ForeignKey("produto.part_number"), nullable=False)

    produto = relationship("Produto", back_populates="historicos")
