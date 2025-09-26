from database import SessionLocal
from models import Tipi, Produto, Historico

def test_connection():

    db = SessionLocal()
    try:
        print("\n📌 Tipi:", db.query(Tipi).count(), "registros encontrados")
        print("📌 Produto:", db.query(Produto).count(), "registros encontrados")
        print("📌 Historico:", db.query(Historico).count(), "registros encontrados")
    except Exception as e:
        print("❌ Erro ao conectar ou consultar:", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
