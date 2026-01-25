from app import app, db, Product, WarehouseStock, StoreStock

with app.app_context():
    # Mannol mahsulotini topish
    p = Product.query.filter(Product.name.ilike('%mannol%')).first()
    
    if p:
        print(f"✓ Mahsulot topildi: {p.name}")
        print(f"  ID: {p.id}")
        print(f"  Unit type: {p.unit_type}")
        print(f"  Cost price: {p.cost_price}")
        print(f"  Sell price: {p.sell_price}")
        
        # Warehouse stocks
        ws = WarehouseStock.query.filter_by(product_id=p.id).all()
        print(f"\n📦 Warehouse stocks: {len(ws)}")
        for s in ws:
            print(f"  - Warehouse {s.warehouse_id}: {s.quantity} {p.unit_type}")
        
        # Store stocks
        ss = StoreStock.query.filter_by(product_id=p.id).all()
        print(f"\n🏪 Store stocks: {len(ss)}")
        for s in ss:
            print(f"  - Store {s.store_id}: {s.quantity} {p.unit_type}")
    else:
        print("✗ Mannol mahsuloti topilmadi")
