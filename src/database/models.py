from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Tipi(Base):
    __tablename__ = "tipi"

    id_tipi = Column(Integer, primary_key=True, index=True)
    descricao = Column(Text, nullable=False)
    aliquota = Column(Numeric(5, 2), nullable=False)
    ncm = Column(String(8), nullable=False)

    produtos = relationship("Produto", back_populates="tipi")


class Endereco(Base):
    __tablename__ = "endereco"

    id_endereco = Column(Integer, primary_key=True, index=True)
    pais_origem = Column(String(80))
    endereco_completo = Column(String(150))

    produtos = relationship("Produto", back_populates="endereco")


class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    part_number = Column(String(25), nullable=False, unique=True)
    descricao = Column(Text)
    fornecedor = Column(String(100))
    status_produto = Column(Boolean, default=False)
    id_tipi = Column(Integer, ForeignKey("tipi.id_tipi"))
    id_endereco = Column(Integer, ForeignKey("endereco.id_endereco"))

    tipi = relationship("Tipi", back_populates="produtos")
    endereco = relationship("Endereco", back_populates="produtos")
    historicos = relationship("Historico", back_populates="produto")


class Historico(Base):
    __tablename__ = "historico"

    id_historico = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hash_code = Column(String(256), nullable=False)
    process_data = Column(DateTime, default=datetime.now)
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False)

    produto = relationship("Produto", back_populates="historicos")
