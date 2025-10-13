from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Tipi(Base):
    __tablename__ = "tipi"

    tipi_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipi_descricao = Column(Text, nullable=False)
    tipi_aliquota = Column(Numeric(5, 2), nullable=False)
    tipi_ncm = Column(Integer, nullable=False)

    produtos = relationship("Produto", back_populates="tipi")


class Fabricante(Base):
    __tablename__ = "fabricante"

    fab_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fab_nome = Column(String(100))
    fab_endereco = Column(String(150))
    fab_pais = Column(String(80))

    produtos = relationship("Produto", back_populates="fabricante")


class Produto(Base):
    __tablename__ = "produto"

    pro_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pro_part_number = Column(String(25), nullable=False, unique=True)
    pro_descricao = Column(Text)
    pro_status = Column(String(20))
    fabricante_fab_id = Column(Integer, ForeignKey("fabricante.fab_id"))
    tipi_tipi_id = Column(Integer, ForeignKey("tipi.tipi_id"))
    historico_hist_id = Column(Integer, ForeignKey("historico.hist_id"))

    tipi = relationship("Tipi", back_populates="produtos")
    fabricante = relationship("Fabricante", back_populates="produtos")
    historicos = relationship("Historico", back_populates="produto")


class Historico(Base):
    __tablename__ = "historico"

    hist_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hist_data_processamento = Column(DateTime, default=datetime.now)
    hist_hash = Column(String(255))

    produto = relationship("Produto", back_populates="historicos")
