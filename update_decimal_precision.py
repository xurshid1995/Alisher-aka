"""
Sale items va sales jadvalidagi DECIMAL ustunlarini kengaytirish
DECIMAL(10,2) -> DECIMAL(12,6) formatiga o'tkazish
"""

from app import app, db
from sqlalchemy import text

def update_decimal_precision():
    with app.app_context():
        try:
            print("🔄 DECIMAL formatlarini yangilamoqda...")
            
            # sale_items jadvali
            queries = [
                # sale_items.cost_price: DECIMAL(10,2) -> DECIMAL(12,6)
                "ALTER TABLE sale_items ALTER COLUMN cost_price TYPE NUMERIC(12,6);",
                
                # sale_items.profit: DECIMAL(12,2) -> DECIMAL(12,6)
                "ALTER TABLE sale_items ALTER COLUMN profit TYPE NUMERIC(12,6);",
                
                # sales.total_cost: DECIMAL(12,2) -> DECIMAL(12,6)
                "ALTER TABLE sales ALTER COLUMN total_cost TYPE NUMERIC(12,6);",
                
                # sales.total_profit: DECIMAL(12,2) -> DECIMAL(12,6)
                "ALTER TABLE sales ALTER COLUMN total_profit TYPE NUMERIC(12,6);",
            ]
            
            for query in queries:
                print(f"📝 Executing: {query}")
                db.session.execute(text(query))
                db.session.commit()
                print("✅ Success!")
            
            print("\n✅ Barcha DECIMAL formatlar yangilandi!")
            print("Endi cost_price va profit 6 xonali kasrli qiymatlarni saqlaydi")
            
        except Exception as e:
            print(f"❌ Xato: {e}")
            db.session.rollback()

if __name__ == "__main__":
    update_decimal_precision()
