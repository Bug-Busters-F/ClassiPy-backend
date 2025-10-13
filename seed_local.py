import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Adiciona o diretório 'src' ao path para permitir a importação dos módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importa as configurações e modelos do seu projeto
from database.config import settings
from database.models import Base, Tipi, Fabricante, Produto, Historico

def seed_data():
    """
    Popula o banco de dados com dados fictícios se ele estiver vazio.
    """
    # Cria a conexão com o banco de dados usando a URL do seu arquivo .env
    engine = create_engine(settings.DATABASE_URL)
    
    # Garante que todas as tabelas definidas nos modelos existam no banco
    Base.metadata.create_all(bind=engine)

    # Cria uma sessão com o banco de dados
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Verifica se a tabela 'tipi' já tem dados para não duplicar
        if db.query(Tipi).count() > 0:
            print("✅ O banco de dados já parece estar populado. Nenhum dado novo foi inserido.")
            return

        print("⏳ Populando o banco de dados com dados fictícios...")

        # 1. Inserindo dados na tabela 'Tipi'
        tipi1 = Tipi(tipi_descricao='Reatores nucleares e suas partes', tipi_aliquota=0.00, tipi_ncm=84011000)
        tipi2 = Tipi(tipi_descricao='Caldeiras de vapor e suas partes', tipi_aliquota=2.50, tipi_ncm=84021100)
        tipi3 = Tipi(tipi_descricao='Motores de pistão de ignição por centelha', tipi_aliquota=3.25, tipi_ncm=84071000)
        db.add_all([tipi1, tipi2, tipi3])
        db.commit()

        # 2. Inserindo dados na tabela 'Fabricante'
        fab1 = Fabricante(fab_nome='Global Parts Co.', fab_endereco='123 Innovation Road, Tech City', fab_pais='China')
        fab2 = Fabricante(fab_nome='American Advanced Motors', fab_endereco='456 Motor Way, Detroit', fab_pais='Estados Unidos')
        fab3 = Fabricante(fab_nome='Deutsche Präzision GmbH', fab_endereco='789 Engineering Strasse, Munich', fab_pais='Alemanha')
        db.add_all([fab1, fab2, fab3])
        db.commit()

        # 3. Inserindo dados na tabela 'Produto', associando com Tipi e Fabricante
        prod1 = Produto(pro_part_number='PN-TESTE-01', pro_descricao='Componente Principal para Reator', pro_status='ATIVO', tipi=tipi1, fabricante=fab1)
        prod2 = Produto(pro_part_number='PN-TESTE-02', pro_descricao='Motor V8 de Alta Performance', pro_status='INATIVO', tipi=tipi3, fabricante=fab2)
        prod3 = Produto(pro_part_number='PN-TESTE-03', pro_descricao='Válvula de Escape para Caldeira', pro_status='ATIVO', tipi=tipi2, fabricante=fab3)
        db.add_all([prod1, prod2, prod3])
        db.commit()

        # 4. Inserindo dados na tabela 'Historico', associando com Produto
        hist1 = Historico(hist_hash='hash_ficticio_para_produto_1_rev1', produto=prod1)
        hist2 = Historico(hist_hash='hash_ficticio_para_produto_1_rev2', produto=prod1)
        hist3 = Historico(hist_hash='hash_ficticio_para_produto_2', produto=prod2)
        hist4 = Historico(hist_hash='hash_ficticio_para_produto_3', produto=prod3)
        db.add_all([hist1, hist2, hist3, hist4])
        db.commit()

        print("🚀 Dados fictícios inseridos com sucesso!")

    except Exception as e:
        print(f"❌ Ocorreu um erro ao inserir os dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    seed_data()