from sqlalchemy.orm import Session
from .. import models
from . import schemes

def createProduto(db: Session, produto_data: schemes.ProductCreate):
    # Cria o Fabricante
    db_fabricante = models.Fabricante(
        fab_nome = produto_data.manufacturer.name,
        fab_pais = produto_data.manufacturer.country,
        fab_endereco = produto_data.manufacturer.address
    )
    db.add(db_fabricante)
    db.commit()
    db.refresh(db_fabricante)

    # Cria o TIPI
    db_tipi = models.Tipi(
        tipi_ncm = produto_data.classification.ncm_code,
        tipi_descricao = produto_data.classification.description,
        tipi_aliquota = produto_data.classification.tax_rate
    )
    db.add(db_tipi)
    db.commit()
    db.refresh(db_tipi)

    # Cria o Produto
    db_produto = models.Produto(
        pro_part_number = produto_data.partNumber,
        pro_descricao = produto_data.description,
        pro_status = 'classificado' if produto_data.status == 'classificado' else 'revisao',
        fabricante_fab_id = db_fabricante.fab_id,
        tipi_tipi_id = db_tipi.tipi_id
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)

    # Cria o Histórico
    db_historico = models.Historico(
        hist_hash = produto_data.fileHash,
        produto_pro_id = db_produto.pro_id
    )
    db.add(db_historico)
    db.commit()
    db.refresh(db_historico)

    # Retorna o histórico, que tem relação com todas as outras tabelas
    return db_historico