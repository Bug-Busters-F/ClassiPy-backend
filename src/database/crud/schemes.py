from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Esquema para os dados do Fabricante
class ManufacturerBase(BaseModel):
    name: str
    country: str
    address: str

# Esquema para os dados da TIPI
class ClassificationBase(BaseModel):
    description: str
    ncm_code: str = Field(alias = 'ncmCode')
    tax_rate: float = Field(alias = 'taxRate')

# Esquema principal para criação de um Produto (API recebe isso)
class ProductCreate(BaseModel):
    partNumber: str
    description: str
    status: str
    classification: ClassificationBase
    manufacturer: ManufacturerBase
    fileHash: str

# Esquemas para resposta da API (modelados pra corresponder ao JSON esperado)
class ResponseManufacturer(BaseModel):
    name: str
    country: str
    address: str

    model_config = {
        "from_attributes": True,
        "populate_by_name":True
        }

class ResponseClassification(BaseModel):
    description: str
    ncmCode: str
    taxRate: float
    manufacturer: ManufacturerBase

    model_config = {
        "from_attributes": True,
        "populate_by_name":True
        }

class HistoryResponse(BaseModel):
    pro_id: Optional[int] = None
    historyId: int
    fileHash: str
    processedDate: datetime
    partNumber: str
    status: str
    classification: Optional[ResponseClassification] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name":True
        }
    
class HistoryCreate(BaseModel):
    partNumber: str
    fileHash: str

class HistoryCreateResponse(BaseModel):
    pro_id: int
    partNumber: str
    fileHash: str
    status: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
    
# Esquema para atualização de um produto 
class ProductUpdate(BaseModel):
    partNumber: str
    description: str
    status: str
    classification: ClassificationBase
    manufacturer: ManufacturerBase

class ClassificationResponse(BaseModel):
    ncm: str
    descricao: str
    fabricante: str
    aliquota: float
    descricao_ncm: str
    
    model_config = {
        "from_attributes": True
    }

class ProductClassificationData(BaseModel):
    ncmCode: str
    description: str
    taxRate: float
    manufacturerName: str
    countryOfOrigin: str
    fullAddress: str

    model_config = {
        "from_attributes": True,
         "populate_by_name": True
    }