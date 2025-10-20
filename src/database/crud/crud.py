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

def deleteProduto(db: Session, produto_id: int):
    # Encontra o produto pelo ID e verifica se existe
    db_produto = db.query(models.Produto).filter(models.Produto.pro_id == produto_id).first()

    if not db_produto:
        return None
    
    # Deleta registros da tabela Histórico que apontam pra esse produto
    db.query(models.Historico).filter(models.Historico.produto_pro_id == produto_id).delete(synchronize_session=False)

    # Deleta o produto e confirma a alteração no banco
    db.delete(db_produto)
    db.commit()

    return db_produto

def updateProduto(db: Session, produto_id: int, produto_data: schemes.ProductUpdate):
    # Encontra o produto pelo ID e verifica se existe
    db_produto = db.query(models.Produto).filter(models.Produto.pro_id == produto_id).first()

    if not db_produto:
        return None
    
    # Acessa as tabelas relacionadas
    db_fabricante = db_produto.fabricante
    db_tipi = db_produto.tipi

    # Atualiza os campos do Produto
    db_produto.pro_part_number = produto_data.partNumber
    db_produto.pro_descricao = produto_data.description
    db_produto.pro_status = produto_data.status

    # Atualiza os campos do Fabricante
    if db_fabricante:
        db_fabricante.fab_nome = produto_data.manufacturer.name
        db_fabricante.fab_pais = produto_data.manufacturer.country
        db_fabricante.fab_endereco = produto_data.manufacturer.address

    # Atualiza os campos da TIPI
    if db_tipi:
        db_tipi.tipi_descricao = produto_data.classification.description
        db_tipi.tipi_ncm = (produto_data.classification.ncm_code)
        db_tipi.tipi_aliquota = produto_data.classification.tax_rate

    # Confirma as alterações e atualiza a tabela Produto
    db.commit()
    db.refresh(db_produto)

    return db_produto

def getProduto(db: Session, produto_id: int):
    # Encontra o produto pelo ID
    return db.query(models.Produto).filter(models.Produto.pro_id == produto_id).first()

def listProdutos(db: Session, skip: int = 0, limit: int = 100):
    # Busca todos os registros da tabela produto
    return db.query(models.Produto).order_by(models.Produto.pro_id.desc()).offset(skip).limit(limit).all()

def listHistorico(db: Session, skip: int = 0, limit: int = 100):
    # Busca todos os registros do histórico, com um limite pra evitar sobrecarga
    return db.query(models.Historico).order_by(models.Historico.hist_id.desc()).offset(skip).limit(limit).all()

# Nova versão da lógica do savePN.py
def saveHistorico(db: Session, part_number: str, file_hash: str):
    # Verifica se o produto já existe
    db_produto = db.query(models.Produto).filter(models.Produto.pro_part_number == part_number).first()

    # Se não existir, cria um novo
    if not db_produto:
        db_produto = models.Produto(
            pro_part_number = part_number,
            pro_status = "revisao",
            tipi_tipi_id = None,
            fabricante_fab_id = None
        )
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)

    # Cria o novo registro de histórico, ligando ao produto
    db_historico = models.Historico(
        hist_hash = file_hash,
        produto_pro_id = db_produto.pro_id
    )
    db.add(db_historico)
    db.commit()
    db.refresh(db_historico)

    return db_produto