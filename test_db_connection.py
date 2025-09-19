from sqlalchemy import text
from src.database import SessionLocal, engine

def test_connection():
    try:
        # Tenta criar uma sessão
        db = SessionLocal()
        print("Sessão com o banco de dados criada com sucesso.")

        # Tenta executar uma query simples
        result = db.execute(text("SELECT 1"))
        print("Query 'SELECT 1' executada com sucesso.")
        
        for row in result:
            print(f"Resultado da query: {row}")

        print("\n\033[92mConexão com o banco de dados funcionando corretamente!\033[0m")

    except Exception as e:
        print(f"\n\033[91mOcorreu um erro ao tentar conectar com o banco de dados:\033[0m")
        print(e)
    finally:
        if 'db' in locals() and db.is_active:
            db.close()
            print("\nSessão com o banco de dados fechada.")

if __name__ == "__main__":
    test_connection()
