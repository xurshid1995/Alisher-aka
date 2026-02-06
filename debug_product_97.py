#!/usr/bin/env python3
"""Debug script - Mahsulot ID 97 va uning stock'larini tekshirish"""

import os
import sys

# Flask app contextini import qilish
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Product, StoreStock, WarehouseStock

def debug_product_97():
    with app.app_context():
        print("=" * 60)
        print("🔍 MAHSULOT ID 97 DEBUG")
        print("=" * 60)
        
        # 1. Mahsulot mavjudligini tekshirish
        product = Product.query.get(97)
        
        if not product:
            print("❌ MAHSULOT TOPILMADI!")
            print("Database'da ID 97 mavjud emas!")
            return
        
        print(f"\n✅ MAHSULOT TOPILDI:")
        print(f"   ID: {product.id}")
        print(f"   Nomi: {product.name}")
        print(f"   Tan narx: ${product.cost_price}")
        print(f"   Sotish narx: ${product.sell_price}")
        print(f"   Barcode: {product.barcode}")
        
        # 2. Store stocks tekshirish
        print(f"\n📦 STORE STOCKS:")
        print("-" * 60)
        
        store_stocks = StoreStock.query.filter_by(product_id=97).all()
        
        if not store_stocks:
            print("   ❌ Store stock'lar topilmadi!")
        else:
            print(f"   Jami {len(store_stocks)} ta store stock qatori:")
            for stock in store_stocks:
                print(f"   • Store ID: {stock.store_id}, Miqdor: {stock.quantity}")
        
        # 3. Warehouse stocks tekshirish  
        print(f"\n📦 WAREHOUSE STOCKS:")
        print("-" * 60)
        
        warehouse_stocks = WarehouseStock.query.filter_by(product_id=97).all()
        
        if not warehouse_stocks:
            print("   ❌ Warehouse stock'lar topilmadi!")
        else:
            print(f"   Jami {len(warehouse_stocks)} ta warehouse stock qatori:")
            for stock in warehouse_stocks:
                print(f"   • Warehouse ID: {stock.warehouse_id}, Miqdor: {stock.quantity}")
        
        # 4. Store ID 2 uchun maxsus tekshirish
        print(f"\n🎯 STORE ID=2 UCHUN TEKSHIRISH:")
        print("-" * 60)
        
        store_2_stock = StoreStock.query.filter_by(
            product_id=97,
            store_id=2
        ).first()
        
        if not store_2_stock:
            print("   ❌ Store ID=2 uchun stock MAVJUD EMAS!")
            print("   Sabab: Bu mahsulot bu do'konda mavjud emas yoki sotib bo'lingan")
        else:
            print(f"   ✅ Store ID=2 uchun stock TOPILDI!")
            print(f"   Miqdor: {store_2_stock.quantity}")
            print(f"   Stock ID: {store_2_stock.id}")
        
        # 5. API filterini simulyatsiya qilish
        print(f"\n🔍 API FILTER SIMULYATSIYASI:")
        print("-" * 60)
        print("   Query: Product.query.filter(Product.store_stocks.any(StoreStock.store_id == 2))")
        
        filtered_products = Product.query.filter(
            Product.store_stocks.any(StoreStock.store_id == 2)
        ).all()
        
        product_ids = [p.id for p in filtered_products]
        
        if 97 in product_ids:
            print(f"   ✅ Mahsulot ID 97 API filter natijasida TOPILDI!")
            print(f"   Jami {len(filtered_products)} ta mahsulot qaytdi")
        else:
            print(f"   ❌ Mahsulot ID 97 API filter natijasida TOPILMADI!")
            print(f"   Jami {len(filtered_products)} ta mahsulot qaytdi")
            print(f"   Sabab: store_stocks.any(store_id==2) false qaytardi")
        
        print("\n" + "=" * 60)

if __name__ == '__main__':
    debug_product_97()
