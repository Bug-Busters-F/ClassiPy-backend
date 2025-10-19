from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import database, models
from ..database.crud import schemes, crud
from typing import List

router = APIRouter(
    prefix="/historico",
    tags=["Histórico"]
)

@router.post("/", response_model = List[schemes.HistoryCreateResponse], status_code = status.HTTP_201_CREATED)
def createHistoryEntries(
    items: List[schemes.HistoryCreate],
    db: Session = Depends(database.get_db)
):
    
    created_items = []
    for item in items:
        # Chama a função do CRUD para cada item da lista
        produto_processado = crud.saveHistorico(
            db = db,
            part_number = item.partNumber,
            file_hash = item.fileHash
        )

        # Adiciona o resultado à lista de resposta
        created_items.append({
            "pro_id": produto_processado.pro_id,
            "partNumber": produto_processado.pro_part_number,
            "fileHash": item.fileHash
        })

    return created_items

@router.delete("/{id}", status_code = 200)
def delProduto(id: int, db: Session = Depends(database.get_db)):
    # Chama a função do CRUD
    db_produto = crud.deleteProduto(db = db, produto_id = id)

    # Exceção caso produto não seja encontrado
    if db_produto is None:
        raise HTTPException(status_code= 404, detail = "Produto não encontrado.")
    
    return {"detail": f"Produto com Part Number '{db_produto.pro_part_number}' e seu histórico foram apagados com sucesso."}

@router.put("/{id}", response_model = schemes.HistoryResponse)
def updProduto(
    id: int,
    produto_update_data: schemes.ProductUpdate,
    db: Session = Depends(database.get_db)
):
    # Chama a função do CRUD
    updated_produto = crud.updateProduto(db = db, produto_id = id, produto_data = produto_update_data)

    # Exceção caso produto não seja encontrado
    if updated_produto is None:
        raise HTTPException(status_code = 404, detail = "Produto não encontrado.")

    # Pega registro de histórico mais recente associado ao produto
    latest_historico = db.query(models.Historico)\
        .filter(models.Historico.produto_pro_id == id)\
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

@router.get("/{id}", response_model = schemes.HistoryResponse)
def readProduto(id: int, db: Session = Depends(database.get_db)):
    # Chama a função do CRUD
    db_produto = crud.getProduto(db = db, produto_id = id)

    # Exceção caso produto não seja encontrado
    if db_produto is None:
        raise HTTPException(status_code = 404, detail = "Produto não encontrado.")
    
    # Pega registro de histórico mais recente associado ao produto
    latest_historico = db.query(models.Historico)\
        .filter(models.Historico.produto_pro_id == id)\
        .order_by(models.Historico.hist_data_processamento.desc())\
        .first()
    
    if not latest_historico:
        raise HTTPException(status_code = 404, detail = "Histórico para esse produto não encontrado.")
    
    # Resposta esperada em JSON
    response = {
        "historyId": latest_historico.hist_id,
        "fileHash": latest_historico.hist_hash,
        "processedDate": latest_historico.hist_data_processamento,
        "partNumber": db_produto.pro_part_number,
        "status": db_produto.pro_status,
        "classification": {
            "description": db_produto.tipi.tipi_descricao,
            "ncmCode": str(db_produto.tipi.tipi_ncm),
            "taxRate": db_produto.tipi.tipi_aliquota,
            "manufacturer": {
                "name": db_produto.fabricante.fab_nome,
                "country": db_produto.fabricante.fab_pais,
                "address": db_produto.fabricante.fab_endereco
            }
        }
    }

    return response

@router.get("/", response_model = list[schemes.HistoryResponse])
def readHistorico(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    historico_list = crud.listHistorico(db, skip = skip, limit = limit)

    results = []
    for historico in historico_list:
        db_produto = historico.produto

        # Monta o objeto de resposta para cada item do histórico
        response_item = {
            "historyId": historico.hist_id,
            "fileHash": historico.hist_hash,
            "processedDate": historico.hist_data_processamento,
            "partNumber": db_produto.pro_part_number,
            "status": db_produto.pro_status,
            "classification": {
                "description": db_produto.tipi.tipi_descricao,
                "ncmCode": str(db_produto.tipi.tipi_ncm),
                "taxRate": db_produto.tipi.tipi_aliquota,
                "manufacturer": {
                    "name": db_produto.fabricante.fab_nome,
                    "country": db_produto.fabricante.fab_pais,
                    "address": db_produto.fabricante.fab_endereco
                }
            }
        }
        results.append(response_item)

    return results