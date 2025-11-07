"""
Test: Foydalanuvchi huquqlarini to'liq tekshirish
"""
from app import app, db, User, Store, Warehouse

with app.app_context():
    print("\n" + "="*80)
    print("TEST 1: Barcha foydalanuvchilarni tekshirish")
    print("="*80)
    
    users = User.query.all()
    for user in users:
        print(f"\n👤 User: {user.username} (ID: {user.id})")
        print(f"   Role: {user.role}")
        print(f"   Permissions: {user.permissions}")
        print(f"   Allowed locations: {user.allowed_locations}")
        print(f"   Transfer locations: {user.transfer_locations}")
        print(f"   Type of allowed_locations: {type(user.allowed_locations)}")
        
        if user.allowed_locations:
            print(f"   Length: {len(user.allowed_locations)}")
            if len(user.allowed_locations) > 0:
                print(f"   First item type: {type(user.allowed_locations[0])}")
                print(f"   First item: {user.allowed_locations[0]}")
    
    print("\n" + "="*80)
    print("TEST 2: extract_location_ids funksiyasini test qilish")
    print("="*80)
    
    from app import extract_location_ids
    
    sotuvchi = User.query.filter_by(username='sotuvchi').first()
    if sotuvchi:
        print(f"\n🧪 Testing sotuvchi user:")
        print(f"   allowed_locations: {sotuvchi.allowed_locations}")
        
        store_ids = extract_location_ids(sotuvchi.allowed_locations, 'store')
        warehouse_ids = extract_location_ids(sotuvchi.allowed_locations, 'warehouse')
        
        print(f"   Extracted store IDs: {store_ids}")
        print(f"   Extracted warehouse IDs: {warehouse_ids}")
        
        # Verify with database
        if store_ids:
            stores = Store.query.filter(Store.id.in_(store_ids)).all()
            print(f"\n   ✅ Stores in database:")
            for s in stores:
                print(f"      - ID={s.id}: {s.name}")
        
        if warehouse_ids:
            warehouses = Warehouse.query.filter(Warehouse.id.in_(warehouse_ids)).all()
            print(f"\n   ✅ Warehouses in database:")
            for w in warehouses:
                print(f"      - ID={w.id}: {w.name}")
    
    print("\n" + "="*80)
    print("TEST 3: Backend API logikasini simulatsiya qilish")
    print("="*80)
    
    if sotuvchi:
        print(f"\n🔍 Simulating /api/locations for sotuvchi:")
        
        allowed_locations = sotuvchi.allowed_locations or []
        print(f"   1. allowed_locations from DB: {allowed_locations}")
        
        allowed_store_ids = extract_location_ids(allowed_locations, 'store')
        allowed_warehouse_ids = extract_location_ids(allowed_locations, 'warehouse')
        
        print(f"   2. Filtered store IDs: {allowed_store_ids}")
        print(f"   3. Filtered warehouse IDs: {allowed_warehouse_ids}")
        
        # Query stores
        if allowed_store_ids:
            stores = Store.query.filter(Store.id.in_(allowed_store_ids)).all()
            print(f"\n   📊 API would return these stores:")
            for s in stores:
                print(f"      - {{'id': {s.id}, 'name': '{s.name}', 'type': 'store'}}")
        else:
            print(f"\n   ⚠️ No stores would be returned")
        
        # Query warehouses
        if allowed_warehouse_ids:
            warehouses = Warehouse.query.filter(Warehouse.id.in_(allowed_warehouse_ids)).all()
            print(f"\n   📊 API would return these warehouses:")
            for w in warehouses:
                print(f"      - {{'id': {w.id}, 'name': '{w.name}', 'type': 'warehouse'}}")
        else:
            print(f"\n   ⚠️ No warehouses would be returned")
