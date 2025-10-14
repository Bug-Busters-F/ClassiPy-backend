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
            "ncmCode": db_historico.produto.tipi.tipi_ncm,
            "taxRate": db_historico.produto.tipi.tipi_aliquota,
            "manufacturer": {
                "name": db_historico.produto.fabricante.fab_nome,
                "country": db_historico.produto.fabricante.fab_pais,
                "addressId": db_historico.produto.fabricante.fab_endereco
            }
        }
    }

    return response