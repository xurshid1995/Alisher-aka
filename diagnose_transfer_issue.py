"""
Transfer muammosini aniqlash va tahlil qilish
Bu skript transfer va stok miqdorlari o'rtasidagi farqlarni topadi
"""
from app import app, db, Transfer, Product, Store, Warehouse, StoreStock, WarehouseStock
from sqlalchemy import func, case
from datetime import datetime, timedelta
from collections import defaultdict

def analyze_transfer_stock_discrepancy():
    """Transfer va stok o'rtasidagi farqlarni tahlil qilish"""
    with app.app_context():
        print("=" * 80)
        print("TRANSFER VA STOK O'RTASIDAGI FARQLARNI TAHLIL QILISH")
        print("=" * 80)
        
        # 1. Har bir mahsulot va do'kon uchun transfer balansini hisoblash
        print("\n" + "=" * 80)
        print("1. TRANSFER BALANSI VA HOZIRGI STOK FARQI")
        print("=" * 80)
        
        # Barcha store_stocks ni olish
        store_stocks = StoreStock.query.all()
        
        discrepancies = []
        
        for stock in store_stocks:
            # Shu mahsulot va do'kon uchun barcha transferlarni hisoblash
            incoming = db.session.query(func.sum(Transfer.quantity)).filter(
                Transfer.product_id == stock.product_id,
                Transfer.to_location_type == 'store',
                Transfer.to_location_id == stock.store_id
            ).scalar() or 0
            
            outgoing = db.session.query(func.sum(Transfer.quantity)).filter(
                Transfer.product_id == stock.product_id,
                Transfer.from_location_type == 'store',
                Transfer.from_location_id == stock.store_id
            ).scalar() or 0
            
            transfer_net = incoming - outgoing
            current_stock = stock.quantity
            difference = abs(current_stock - transfer_net)
            
            # Agar farq bo'lsa va muhim bo'lsa (1 dan katta)
            if difference > 1:
                product = Product.query.get(stock.product_id)
                store = Store.query.get(stock.store_id)
                
                discrepancies.append({
                    'product': product.name if product else 'N/A',
                    'barcode': product.barcode if product else 'N/A',
                    'store': store.name if store else 'N/A',
                    'current_stock': current_stock,
                    'incoming_transfers': incoming,
                    'outgoing_transfers': outgoing,
                    'transfer_net': transfer_net,
                    'difference': difference
                })
        
        # Farqlarni farq bo'yicha saralash
        discrepancies.sort(key=lambda x: x['difference'], reverse=True)
        
        # Eng katta farqlarni ko'rsatish
        print(f"\nJAMI {len(discrepancies)} ta mahsulot-do'kon juftligida farq topildi")
        print(f"\nENG KATTA 20 TA FARQ:\n")
        
        for i, disc in enumerate(discrepancies[:20], 1):
            print(f"{i}. {disc['product']} ({disc['barcode']}) - {disc['store']}")
            print(f"   Hozirgi stok: {disc['current_stock']}")
            print(f"   Transfer kirim: +{disc['incoming_transfers']}")
            print(f"   Transfer chiqim: -{disc['outgoing_transfers']}")
            print(f"   Transfer netto: {disc['transfer_net']}")
            print(f"   FARQ: {disc['difference']}")
            print()
        
        # 2. Oxirgi transferlarni ko'rsatish
        print("\n" + "=" * 80)
        print("2. OXIRGI 20 TA TRANSFER")
        print("=" * 80)
        
        recent_transfers = Transfer.query.order_by(Transfer.created_at.desc()).limit(20).all()
        
        for i, transfer in enumerate(recent_transfers, 1):
            product = Product.query.get(transfer.product_id)
            print(f"\n{i}. Transfer ID: {transfer.id}")
            print(f"   Mahsulot: {product.name if product else 'N/A'}")
            print(f"   Qayerdan: {transfer.from_location_type}_{transfer.from_location_id} ({transfer.from_location_name})")
            print(f"   Qayerga: {transfer.to_location_type}_{transfer.to_location_id} ({transfer.to_location_name})")
            print(f"   Miqdor: {transfer.quantity}")
            print(f"   Vaqt: {transfer.created_at}")
            print(f"   Foydalanuvchi: {transfer.user_name}")
        
        # 3. Transferlar statistikasi
        print("\n" + "=" * 80)
        print("3. TRANSFERLAR STATISTIKASI (oxirgi 40 kun)")
        print("=" * 80)
        
        forty_days_ago = datetime.now() - timedelta(days=40)
        
        total_transfers = Transfer.query.filter(Transfer.created_at >= forty_days_ago).count()
        
        store_to_store = Transfer.query.filter(
            Transfer.created_at >= forty_days_ago,
            Transfer.from_location_type == 'store',
            Transfer.to_location_type == 'store'
        ).count()
        
        warehouse_to_store = Transfer.query.filter(
            Transfer.created_at >= forty_days_ago,
            Transfer.from_location_type == 'warehouse',
            Transfer.to_location_type == 'store'
        ).count()
        
        store_to_warehouse = Transfer.query.filter(
            Transfer.created_at >= forty_days_ago,
            Transfer.from_location_type == 'store',
            Transfer.to_location_type == 'warehouse'
        ).count()
        
        warehouse_to_warehouse = Transfer.query.filter(
            Transfer.created_at >= forty_days_ago,
            Transfer.from_location_type == 'warehouse',
            Transfer.to_location_type == 'warehouse'
        ).count()
        
        print(f"\nJAMI transferlar: {total_transfers}")
        print(f"Do'kondan do'konga: {store_to_store}")
        print(f"Ombordan do'konga: {warehouse_to_store}")
        print(f"Do'kondan omborga: {store_to_warehouse}")
        print(f"Ombordan omborga: {warehouse_to_warehouse}")
        
        # 4. Eng ko'p transfer qilingan mahsulotlar
        print("\n" + "=" * 80)
        print("4. ENG KO'P TRANSFER QILINGAN 10 TA MAHSULOT")
        print("=" * 80)
        
        product_transfer_counts = db.session.query(
            Transfer.product_id,
            func.count(Transfer.id).label('transfer_count'),
            func.sum(Transfer.quantity).label('total_quantity')
        ).filter(
            Transfer.created_at >= forty_days_ago
        ).group_by(
            Transfer.product_id
        ).order_by(
            func.count(Transfer.id).desc()
        ).limit(10).all()
        
        for i, (product_id, count, total_qty) in enumerate(product_transfer_counts, 1):
            product = Product.query.get(product_id)
            print(f"\n{i}. {product.name if product else 'N/A'} ({product.barcode if product else 'N/A'})")
            print(f"   Transfer soni: {count}")
            print(f"   Jami miqdor: {total_qty}")
        
        # 5. Har bir do'kon uchun stok va transfer balansi
        print("\n" + "=" * 80)
        print("5. HAR BIR DO'KON UCHUN STOK VA TRANSFER BALANSI")
        print("=" * 80)
        
        stores = Store.query.all()
        
        for store in stores:
            # Shu do'kondagi jami stok
            total_stock = db.session.query(func.sum(StoreStock.quantity)).filter(
                StoreStock.store_id == store.id
            ).scalar() or 0
            
            # Shu do'konga kirim transferlar
            incoming = db.session.query(func.sum(Transfer.quantity)).filter(
                Transfer.to_location_type == 'store',
                Transfer.to_location_id == store.id,
                Transfer.created_at >= forty_days_ago
            ).scalar() or 0
            
            # Shu do'kondan chiqim transferlar
            outgoing = db.session.query(func.sum(Transfer.quantity)).filter(
                Transfer.from_location_type == 'store',
                Transfer.from_location_id == store.id,
                Transfer.created_at >= forty_days_ago
            ).scalar() or 0
            
            print(f"\n{store.name} (ID: {store.id})")
            print(f"   Jami hozirgi stok: {total_stock}")
            print(f"   Transfer kirim (40 kun): +{incoming}")
            print(f"   Transfer chiqim (40 kun): -{outgoing}")
            print(f"   Transfer netto: {incoming - outgoing}")

if __name__ == '__main__':
    analyze_transfer_stock_discrepancy()
