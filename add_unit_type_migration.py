# -*- coding: utf-8 -*-
"""
Migration: O'lchov birligi (unit_type) qo'shish
- products jadvaliga unit_type ustuni qo'shish
- Barcha quantity ustunlarini DECIMAL ga o'zgartirish
"""
from app import app, db
from sqlalchemy import text
import sys

def run_migration():
    """Migration ni bajarish"""
    with app.app_context():
        try:
            print("\n" + "="*60)
            print("🚀 O'lchov birligi (Unit Type) Migration Boshlandi")
            print("="*60 + "\n")
            
            # 1. Products jadvaliga unit_type ustuni qo'shish
            print("📝 1. Products jadvaliga unit_type ustuni qo'shilmoqda...")
            try:
                db.session.execute(text("""
                    ALTER TABLE products 
                    ADD COLUMN IF NOT EXISTS unit_type VARCHAR(10) DEFAULT 'dona' NOT NULL
                """))
                db.session.commit()
                print("   ✅ Products.unit_type qo'shildi (default: 'dona')")
            except Exception as e:
                print(f"   ⚠️ Products.unit_type: {str(e)}")
                db.session.rollback()
            
            # 2. WarehouseStock quantity ni DECIMAL ga o'zgartirish
            print("\n📝 2. WarehouseStock.quantity ni DECIMAL ga o'zgartirish...")
            try:
                db.session.execute(text("""
                    ALTER TABLE warehouse_stocks 
                    ALTER COLUMN quantity TYPE DECIMAL(10, 2)
                """))
                db.session.commit()
                print("   ✅ WarehouseStock.quantity DECIMAL(10,2) ga o'zgartirildi")
            except Exception as e:
                print(f"   ⚠️ WarehouseStock.quantity: {str(e)}")
                db.session.rollback()
            
            # 3. StoreStock quantity ni DECIMAL ga o'zgartirish
            print("\n📝 3. StoreStock.quantity ni DECIMAL ga o'zgartirish...")
            try:
                db.session.execute(text("""
                    ALTER TABLE store_stocks 
                    ALTER COLUMN quantity TYPE DECIMAL(10, 2)
                """))
                db.session.commit()
                print("   ✅ StoreStock.quantity DECIMAL(10,2) ga o'zgartirildi")
            except Exception as e:
                print(f"   ⚠️ StoreStock.quantity: {str(e)}")
                db.session.rollback()
            
            # 4. SaleItems quantity ni DECIMAL ga o'zgartirish
            print("\n📝 4. SaleItems.quantity ni DECIMAL ga o'zgartirish...")
            try:
                db.session.execute(text("""
                    ALTER TABLE sale_items 
                    ALTER COLUMN quantity TYPE DECIMAL(10, 2)
                """))
                db.session.commit()
                print("   ✅ SaleItems.quantity DECIMAL(10,2) ga o'zgartirildi")
            except Exception as e:
                print(f"   ⚠️ SaleItems.quantity: {str(e)}")
                db.session.rollback()
            
            # 5. Transfers quantity ni DECIMAL ga o'zgartirish
            print("\n📝 5. Transfers.quantity ni DECIMAL ga o'zgartirish...")
            try:
                db.session.execute(text("""
                    ALTER TABLE transfers 
                    ALTER COLUMN quantity TYPE DECIMAL(10, 2)
                """))
                db.session.commit()
                print("   ✅ Transfers.quantity DECIMAL(10,2) ga o'zgartirildi")
            except Exception as e:
                print(f"   ⚠️ Transfers.quantity: {str(e)}")
                db.session.rollback()
            
            # 6. Orders quantity ni DECIMAL ga o'zgartirish
            print("\n📝 6. Orders.quantity ni DECIMAL ga o'zgartirish...")
            try:
                db.session.execute(text("""
                    ALTER TABLE orders 
                    ALTER COLUMN quantity TYPE DECIMAL(10, 2)
                """))
                db.session.commit()
                print("   ✅ Orders.quantity DECIMAL(10,2) ga o'zgartirildi")
            except Exception as e:
                print(f"   ⚠️ Orders.quantity: {str(e)}")
                db.session.rollback()
            
            # 7. Verification - O'zgarishlarni tekshirish
            print("\n📊 7. Verification - O'zgarishlarni tekshirish...")
            result = db.session.execute(text("""
                SELECT 
                    column_name, 
                    data_type,
                    character_maximum_length,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = 'products' 
                    AND column_name = 'unit_type'
            """))
            
            row = result.fetchone()
            if row:
                print(f"   ✅ Products.unit_type: {row[1]} (default: {row[3]})")
            else:
                print("   ❌ Products.unit_type topilmadi!")
            
            # Quantity ustunlarini tekshirish
            tables = ['warehouse_stocks', 'store_stocks', 'sale_items', 'transfers', 'orders']
            for table in tables:
                result = db.session.execute(text(f"""
                    SELECT data_type, numeric_precision, numeric_scale
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' 
                        AND column_name = 'quantity'
                """))
                row = result.fetchone()
                if row:
                    print(f"   ✅ {table}.quantity: {row[0]} ({row[1]},{row[2]})")
            
            print("\n" + "="*60)
            print("✅ Migration muvaffaqiyatli yakunlandi!")
            print("="*60 + "\n")
            
            print("📌 Keyingi qadamlar:")
            print("   1. app.py dagi model larni yangilang")
            print("   2. Frontend da unit_type tanlash qo'shing")
            print("   3. Validatsiya logikasini qo'shing\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Migration xatolik bilan yakunlandi: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    run_migration()
