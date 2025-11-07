"""
Recreate warehouses with correct IDs (1001+)
"""
from app import app, db, Warehouse
from sqlalchemy import text

with app.app_context():
    print("\n" + "="*80)
    print("RECREATING WAREHOUSES WITH NEW IDS")
    print("="*80)
    
    # Create warehouses with new IDs
    warehouses_data = [
        {'id': 1001, 'name': 'UY Sergeli', 'address': 'Sergeli tumani', 'manager_name': 'Manager 1', 'phone': '+998901234567'},
        {'id': 1002, 'name': 'Akfa', 'address': 'Akfa hududida', 'manager_name': 'Manager 2', 'phone': '+998901234568'},
    ]
    
    for data in warehouses_data:
        # Check if exists
        existing = Warehouse.query.get(data['id'])
        if existing:
            print(f"⚠️ Warehouse ID={data['id']} already exists: {existing.name}")
            continue
        
        # Create new
        warehouse = Warehouse(
            name=data['name'],
            address=data['address'],
            manager_name=data['manager_name'],
            phone=data['phone'],
            current_stock=0
        )
        db.session.add(warehouse)
        db.session.flush()  # Get ID
        
        # Update ID manually
        db.session.execute(text(f"UPDATE warehouses SET id = {data['id']} WHERE id = {warehouse.id}"))
        
        print(f"✅ Created warehouse: ID={data['id']}, Name={data['name']}")
    
    # Set auto-increment
    db.session.execute(text("ALTER SEQUENCE warehouses_id_seq RESTART WITH 1003"))
    
    db.session.commit()
    
    print(f"\n✅ Done! Auto-increment set to 1003")
    
    # Verify
    warehouses = Warehouse.query.all()
    print(f"\n📦 Verification - Total warehouses: {len(warehouses)}")
    for w in warehouses:
        print(f"  - ID={w.id}, Name={w.name}")
