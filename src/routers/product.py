from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import database, models
from ..database.crud import schemes, crud
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/produto",
    tags=["Produto"]
)

router_historico = APIRouter(
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
        try:
            # Chama a função do CRUD para cada item da lista
            produto_processado = crud.saveHistorico(
                db = db,
                part_number = item.partNumber,
                file_hash = item.fileHash
            )

            # Adiciona o resultado à lista de resposta
            response_item = {
                "pro_id": produto_processado["pro_id"],
                "partNumber": produto_processado["partNumber"],
                "fileHash": item.fileHash,
                "status": produto_processado["status"]
            }
            created_items.append(response_item)

        except Exception as e:
            raise HTTPException(
                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail=f"Erro ao processar o Part Number {item.partNumber}: {str(e)}"
            )

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
    
    classification_data = None
    if db_produto.tipi and db_produto.fabricante:
        classification_data = {
            "description": db_produto.tipi.tipi_descricao,
            "ncmCode": str(db_produto.tipi.tipi_ncm),
            "taxRate": db_produto.tipi.tipi_aliquota,
            "manufacturer": {
                "name": db_produto.fabricante.fab_nome,
                "country": db_produto.fabricante.fab_pais,
                "address": db_produto.fabricante.fab_endereco
            }
        }

    # Resposta esperada em JSON
    response = {
        "historyId": latest_historico.hist_id,
        "fileHash": latest_historico.hist_hash,
        "processedDate": latest_historico.hist_data_processamento,
        "partNumber": db_produto.pro_part_number,
        "status": db_produto.pro_status,
        "classification": classification_data
    }

    return response

@router_historico.get("/", response_model = list[schemes.HistoryResponse])
def readHistorico(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    filter_date: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    print(f"DEBUG: Recebido search='{search}' e filter_date='{filter_date}'")
    # Tratamento das datas
    dt_start = None
    dt_end = None

    if filter_date:
        try:
            date_obj = datetime.strptime(filter_date, "%Y-%m-%d")
            dt_start = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            dt_end = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            pass

    historico_list = crud.listHistorico(
        db, 
        skip = skip, 
        limit = limit,
        search = search,
        start_date = dt_start,
        end_date = dt_end
    )

    results = []
    for historico in historico_list:
        db_produto = historico.produto

        classification_data = None
        # Monta o objeto de resposta para cada item do histórico
        if db_produto.tipi and db_produto.fabricante:
            classification_data = {
                "description": db_produto.tipi.tipi_descricao,
                "ncmCode": str(db_produto.tipi.tipi_ncm),
                "taxRate": db_produto.tipi.tipi_aliquota,
                "manufacturer": {
                    "name": db_produto.fabricante.fab_nome,
                    "country": db_produto.fabricante.fab_pais,
                    "address": db_produto.fabricante.fab_endereco
                }
            }

        response_item = {
            "historyId": historico.hist_id,
            "fileHash": historico.hist_hash,
            "processedDate": historico.hist_data_processamento,
            "partNumber": db_produto.pro_part_number,
            "status": db_produto.pro_status,
            "classification": classification_data
        }
        results.append(response_item)

    return results

@router_historico.delete("/{history_id}", status_code = status.HTTP_200_OK)
def deleteHistory(history_id: int, db: Session = Depends(database.get_db)):
    deleted_item = crud.deleteHistorico(db=db, history_id=history_id)

    if deleted_item is None:
        raise HTTPException(status_code=404, detail = "Entrada de histórico não encontrada.")
    
    return {"detail": f"Entrada do histórico {history_id} excluída com sucesso."}

@router.get("/{pro_id}/classification", response_model=schemes.ProductClassificationData, status_code=status.HTTP_200_OK)
def getProductClassificationData(
    pro_id: int,
    db: Session = Depends(database.get_db)
):
    # Buscar os dados de classificação de um produto já existente.
    try:
        classification = crud.getProdutoClassification(db=db, pro_id=pro_id)

        if classification is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dados de classificação não encontrados para o produto com ID {pro_id}."
            )
        
        return classification

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar dados de classificação: {str(e)}"
        )