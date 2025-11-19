from sqlalchemy.orm import Session, joinedload
from .. import models
from . import schemes
from src.database.models import Produto, Historico
from typing import List

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
    db_produto = db.query(models.Produto).options(
        joinedload(models.Produto.tipi), 
        joinedload(models.Produto.fabricante)
    ).filter(models.Produto.pro_id == produto_id).first()

    if not db_produto:
        return None
    
    db_tipi = db.query(models.Tipi).filter(models.Tipi.tipi_ncm == produto_data.classification.ncm_code).first()
    
    if not db_tipi:
        db_tipi = models.Tipi(
            tipi_ncm = produto_data.classification.ncm_code,
            tipi_descricao = produto_data.classification.description,
            tipi_aliquota = produto_data.classification.tax_rate
        )
        db.add(db_tipi)
        db.flush()
    else:
        db_tipi.tipi_descricao = produto_data.classification.description
        db_tipi.tipi_aliquota = produto_data.classification.tax_rate

    db_fabricante = db.query(models.Fabricante).filter(models.Fabricante.fab_nome == produto_data.manufacturer.name).first()

    if not db_fabricante:
        db_fabricante = models.Fabricante(
            fab_nome = produto_data.manufacturer.name,
            fab_pais = produto_data.manufacturer.country,
            fab_endereco = produto_data.manufacturer.address
        )
        db.add(db_fabricante)
        db.flush() 
    else:
        db_fabricante.fab_pais = produto_data.manufacturer.country
        db_fabricante.fab_endereco = produto_data.manufacturer.address

    db_produto.pro_part_number = produto_data.partNumber
    db_produto.pro_descricao = produto_data.description
    db_produto.pro_status = produto_data.status
    
    db_produto.tipi = db_tipi             
    db_produto.fabricante = db_fabricante 
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
    try:
        # Verifica se o produto já existe
        db_produto = db.query(models.Produto).filter(models.Produto.pro_part_number == part_number).first()

        product_status = "revisao"

        # Se não existir, cria um novo
        if not db_produto:
            db_produto = models.Produto(
                pro_part_number = part_number,
                pro_status = "revisao",
                tipi_tipi_id = None,
                fabricante_fab_id = None
            )
            db.add(db_produto)
            db.flush()
        else:
            product_status = db_produto.pro_status

        # Cria o novo registro de histórico, ligando ao produto
        db_historico = db.query(models.Historico).filter(
            models.Historico.hist_hash == file_hash, 
            models.Historico.produto_pro_id == db_produto.pro_id).first()

        if not db_historico:
            db_historico = models.Historico(
                hist_hash = file_hash,
                produto_pro_id = db_produto.pro_id
            )
            db.add(db_historico)
            db.commit()
            db.refresh(db_produto)
            db.refresh(db_historico)

        return {
            "pro_id": db_produto.pro_id,
            "partNumber": db_produto.pro_part_number,
            "status": product_status
        }
    
    # Caso dê errado, desfaz as mudanças e propaga o erro
    except Exception as e:
        db.rollback()
        raise e
    
def getProdutoClassification(db: Session, pro_id: int):
    # Busca os dados de classificação de um produto pelo seu ID.
    try:
        db_produto = db.query(models.Produto).filter(models.Produto.pro_id == pro_id).first()
        if not db_produto:
            return None

        # Se o produto não tiver ID de fabricante ou tipi, significa que não foi classificado
        if not db_produto.fabricante_fab_id or not db_produto.tipi_tipi_id:
             return None

        db_fabricante = db.query(models.Fabricante).filter(
            models.Fabricante.fab_id == db_produto.fabricante_fab_id).first()

        db_tipi = db.query(models.Tipi).filter(
            models.Tipi.tipi_id == db_produto.tipi_tipi_id).first()

        if not db_fabricante or not db_tipi:
             return None

        classification_data = {
            "ncmCode": db_tipi.tipi_ncm,
            "description": db_tipi.tipi_descricao,
            "taxRate": db_tipi.tipi_aliquota,
            "manufacturerName": db_fabricante.fab_nome,
            "countryOfOrigin": db_fabricante.fab_pais,
            "fullAddress": db_fabricante.fab_endereco
        }
        return classification_data

    except Exception as e:
        print(f"❌ Erro em get_produto_classification para pro_id {pro_id}: {e}")
        raise e

def fetch_recent_products(db: Session, limit: int = 5) -> List[dict]:
    # Subquery para pegar o histórico mais recente de cada produto
    subquery = (
        db.query(
            Historico.produto_pro_id,
            Historico.hist_id,
            Historico.hist_data_processamento,
            Historico.hist_hash
        )
        .order_by(Historico.produto_pro_id, Historico.hist_data_processamento.desc())
        .distinct(Historico.produto_pro_id)
        .subquery()
    )

    # Query principal, trazendo Produto + Histórico + Tipi + Fabricante
    results = (
        db.query(Produto, subquery.c.hist_id, subquery.c.hist_data_processamento, subquery.c.hist_hash)
        .join(subquery, Produto.pro_id == subquery.c.produto_pro_id)
        .outerjoin(Produto.tipi)
        .outerjoin(Produto.fabricante)
        .order_by(subquery.c.hist_data_processamento.desc())
        .limit(limit)
        .all()
    )

    # Monta a resposta
    response = []
    for produto, hist_id, processed_date, file_hash in results:
        response.append({
            "pro_id": produto.pro_id,
            "historyId": hist_id,
            "fileHash": file_hash,
            "processedDate": processed_date.isoformat() if processed_date else None,
            "partNumber": produto.pro_part_number,
            "status": produto.pro_status,
            "classification": {
                "description": produto.tipi.tipi_descricao if produto.tipi else None,
                "ncmCode": produto.tipi.tipi_ncm if produto.tipi else None,
                "taxRate": float(produto.tipi.tipi_aliquota) if produto.tipi else None,
                "manufacturer": {
                    "name": produto.fabricante.fab_nome if produto.fabricante else None,
                    "country": produto.fabricante.fab_pais if produto.fabricante else None,
                    "address": produto.fabricante.fab_endereco if produto.fabricante else None
                } if produto.fabricante else None
            }
        })
    return response