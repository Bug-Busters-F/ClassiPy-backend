from ..database.database import SessionLocal
from ..database.models import Historico, Produto
from datetime import datetime

def save_history(part_number: str, hash_code: str):
    db = SessionLocal()
    try:
        product = db.query(Produto).filter_by(part_number=part_number).first()
        
        if not product:
            product = Produto(part_number=part_number)
            db.add(product)
            db.commit()
            db.refresh(product)
            print(f"✅ Product created with part_number={product.part_number}")

        new_history = Historico(
            produto_id=product.id,
            hash_code=hash_code,
            process_data=datetime.now()
        )
        db.add(new_history)
        db.commit()
        db.refresh(new_history)

        print(f"✅ History saved: id={new_history.id_historico}, product_id={new_history.produto_id}, hash={new_history.hash_code}")
        return new_history
    
    except Exception as e:
        db.rollback()
        print("❌ Error saving history:", e)
        return None
    finally:
        db.close()



