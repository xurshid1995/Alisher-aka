from app import app, db
import sqlalchemy as sa
from sqlalchemy import text

with app.app_context():
    try:
        # Seller_id ustunini qo'shish
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE sales ADD COLUMN seller_id INTEGER REFERENCES users(id)'))
            conn.commit()
        print('✅ seller_id ustuni muvaffaqiyatli qo\'shildi')
    except Exception as e:
        print(f'⚠️ Ustun qo\'shish xatoligi (ehtimol allaqachon mavjud): {e}')
    
    try:
        # Mavjud savdolarga admin user ni belgilash  
        with db.engine.connect() as conn:
            result = conn.execute(text('UPDATE sales SET seller_id = 1 WHERE seller_id IS NULL'))
            conn.commit()
            print(f'✅ {result.rowcount} ta savdo uchun seller_id yangilandi')
    except Exception as e:
        print(f'⚠️ Update xatoligi: {e}')
    
    print('✅ Migration yakunlandi!')