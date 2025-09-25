from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Tipi(Base):
    __tablename__ = "tipi"

    id_tipi = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(100))
    aliquota = Column(Numeric(5, 2))
    ncm = Column(String(8))

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

    hash_code = Column(String(256))
    process_data = Column(Date)
    part_number = Column(String(25), ForeignKey("produto.part_number"), primary_key=True)

    produto = relationship("Produto", back_populates="historicos")
