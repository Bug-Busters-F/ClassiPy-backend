from database import SessionLocal, engine
from models import Tipi, Endereco, Produto, Historico, Base

def seed_data():
    # Cria as tabelas no banco de dados (se não existirem)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Verifica se já existem dados para não duplicar
        if db.query(Tipi).count() == 0:
            print("Populando o banco de dados com dados fictícios...")

            # Adiciona dados para Tipi
            tipi1 = Tipi(descricao='Reatores nucleares...', aliquota=0.00, ncm='84011000')
            tipi2 = Tipi(descricao='Caldeiras de vapor...', aliquota=0.00, ncm='84021100')
            tipi3 = Tipi(descricao='Motores de explosão...', aliquota=3.25, ncm='84071000')
            db.add_all([tipi1, tipi2, tipi3])
            db.commit()

            # Adiciona dados para Endereco
            end1 = Endereco(pais_origem='China', endereco_completo='123 Ling Ling Street, Shanghai, China')
            end2 = Endereco(pais_origem='Estados Unidos', endereco_completo='456 Innovation Drive, Silicon Valley, USA')
            end3 = Endereco(pais_origem='Alemanha', endereco_completo='789 Autobahn Avenue, Berlin, Germany')
            db.add_all([end1, end2, end3])
            db.commit()

            # Adiciona dados para Produto
            prod1 = Produto(part_number='PN-12345-A', descricao='Componente Eletrônico Principal', fornecedor='Fornecedor A', status_produto=True, id_tipi=tipi1.id_tipi, id_endereco=end1.id_endereco)
            prod2 = Produto(part_number='PN-67890-B', descricao='Motor de Alta Performance', fornecedor='Fornecedor B', status_produto=False, id_tipi=tipi3.id_tipi, id_endereco=end3.id_endereco)
            prod3 = Produto(part_number='PN-ABCDE-C', descricao='Peça Mecânica de Precisão', fornecedor='Fornecedor C', status_produto=True, id_tipi=tipi2.id_tipi, id_endereco=end2.id_endereco)
            db.add_all([prod1, prod2, prod3])
            db.commit()

            # Adiciona dados para Historico
            hist1 = Historico(hash_code='hash_para_produto_1_rev1', produto_id=prod1.id)
            hist2 = Historico(hash_code='hash_para_produto_1_rev2', produto_id=prod1.id)
            hist3 = Historico(hash_code='hash_para_produto_2', produto_id=prod2.id)
            hist4 = Historico(hash_code='hash_para_produto_3', produto_id=prod3.id)
            db.add_all([hist1, hist2, hist3, hist4])
            db.commit()

            print("Dados fictícios inseridos com sucesso!")
        else:
            print("O banco de dados já parece estar populado. Nenhum dado foi inserido.")

    except Exception as e:
        print(f"Ocorreu um erro ao inserir os dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()