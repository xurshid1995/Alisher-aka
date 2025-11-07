"""
Verify that the warehouse ID migration and permission fix are complete.
"""

from app import app, db, User, Store, Warehouse

def main():
    with app.app_context():
        print("\n" + "="*60)
        print("VERIFICATION REPORT")
        print("="*60)
        
        # Check stores
        print("\n📦 STORES:")
        stores = Store.query.all()
        for store in stores:
            print(f"  - ID={store.id}, Name={store.name}")
        
        # Check warehouses
        print("\n🏭 WAREHOUSES:")
        warehouses = Warehouse.query.all()
        for wh in warehouses:
            print(f"  - ID={wh.id}, Name={wh.name}")
        
        # Check sotuvchi permissions
        print("\n👤 SOTUVCHI USER:")
        sotuvchi = User.query.filter_by(username='sotuvchi').first()
        if sotuvchi:
            print(f"\n  allowed_locations ({len(sotuvchi.allowed_locations)} locations):")
            for loc in sotuvchi.allowed_locations:
                loc_type = loc['type']
                loc_id = loc['id']
                
                if loc_type == 'store':
                    store = Store.query.get(loc_id)
                    name = store.name if store else "NOT FOUND"
                elif loc_type == 'warehouse':
                    wh = Warehouse.query.get(loc_id)
                    name = wh.name if wh else "NOT FOUND"
                
                print(f"    - {loc_type.upper()} ID={loc_id} ({name})")
            
            print(f"\n  transfer_locations ({len(sotuvchi.transfer_locations)} locations):")
            for loc in sotuvchi.transfer_locations:
                loc_type = loc['type']
                loc_id = loc['id']
                
                if loc_type == 'store':
                    store = Store.query.get(loc_id)
                    name = store.name if store else "NOT FOUND"
                elif loc_type == 'warehouse':
                    wh = Warehouse.query.get(loc_id)
                    name = wh.name if wh else "NOT FOUND"
                
                print(f"    - {loc_type.upper()} ID={loc_id} ({name})")
        else:
            print("  ❌ User not found!")
        
        print("\n" + "="*60)
        print("✅ VERIFICATION COMPLETE")
        print("="*60)
        print("\n📊 Summary:")
        print(f"  - Total stores: {len(stores)}")
        print(f"  - Total warehouses: {len(warehouses)}")
        print(f"  - sotuvchi locations: {len(sotuvchi.allowed_locations) if sotuvchi else 0}")
        
        # Check for ID conflicts
        store_ids = {s.id for s in stores}
        warehouse_ids = {w.id for w in warehouses}
        conflicts = store_ids & warehouse_ids
        
        if conflicts:
            print(f"\n⚠️ WARNING: ID conflicts detected: {conflicts}")
        else:
            print("\n✅ No ID conflicts between stores and warehouses!")

if __name__ == '__main__':
    main()
