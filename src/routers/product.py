from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import database, models
from ..database.crud import schemes, crud

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

@router.post("/", response_model = schemes.HistoryResponse)
def addProduto(
    produto: schemes.ProductCreate,
    db: Session = Depends(database.get_db)
):
    db_produto_existente = db.query(models.Produto).filter(models.Produto.pro_part_number == produto.partNumber).first()
    if db_produto_existente:
        raise HTTPException(status_code = 400, detail = "Part Number já cadastrado.")
    
    # Chamando a função do CRUD
    db_historico = crud.createProduto(db = db, produto_data = produto)

    # Resposta esperada em JSON
    response = {
        "historyId": db_historico.hist_id,
        "fileHash": db_historico.hist_hash,
        "processedDate": db_historico.hist_data_processamento,
        "partNumber": db_historico.produto.pro_part_number,
        "status": db_historico.produto.pro_status,
        "classification": {
            "description": db_historico.produto.tipi.tipi_descricao,
            "ncmCode": str(db_historico.produto.tipi.tipi_ncm),
            "taxRate": db_historico.produto.tipi.tipi_aliquota,
            "manufacturer": {
                "name": db_historico.produto.fabricante.fab_nome,
                "country": db_historico.produto.fabricante.fab_pais,
                "address": db_historico.produto.fabricante.fab_endereco
            }
        }
    }

    return response

@router.delete("/{produto_id}", status_code = 200)
def delProduto(produto_id: int, db: Session = Depends(database.get_db)):
    # Chama a função do CRUD
    db_produto = crud.deleteProduto(db = db, produto_id = produto_id)

    # Exceção caso produto não seja encontrado
    if db_produto is None:
        raise HTTPException(status_code= 404, detail = "Produto não encontrado.")
    
    return {"detail": f"Produto com Part Number '{db_produto.pro_part_number}' e seu histórico foram apagados com sucesso."}

@router.put("/{produto.id}", response_model = schemes.HistoryResponse)
def updProduto(
    produto_id: int,
    produto_update_data: schemes.ProductUpdate,
    db: Session = Depends(database.get_db)
):
    # Chama a função do CRUD
    updated_produto = crud.updateProduto(db = db, produto_id = produto_id, produto_data = produto_update_data)

    # Exceção caso produto não seja encontrado
    if updated_produto is None:
        raise HTTPException(status_code = 404, detail = "Produto não encontrado.")

    # Pega registro de histórico mais recente associado ao produto
    latest_historico = db.query(models.Historico)\
        .filter(models.Historico.produto_pro_id == produto_id)\
        .order_by(models.Historico.hist_data_processamento.desc())\
        .first()
    
    if not latest_historico:
        raise HTTPException(status_code = 404, detail = "Histórico para esse produto não encontrado.")

    # Resposta esperada em JSON
    response = {
        "historyId": latest_historico.hist_id,
        "fileHash": latest_historico.hist_hash,
        "processedDate": latest_historico.hist_data_processamento,
        "partNumber": updated_produto.pro_part_number,
        "status": updated_produto.pro_status,
        "classification": {
            "description": updated_produto.tipi.tipi_descricao,
            "ncmCode": str(updated_produto.tipi.tipi_ncm),
            "taxRate": updated_produto.tipi.tipi_aliquota,
            "manufacturer": {
                "name": updated_produto.fabricante.fab_nome,
                "country": updated_produto.fabricante.fab_pais,
                "address": updated_produto.fabricante.fab_endereco
            }
        }
    }

    return response