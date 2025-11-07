"""
Migration: Warehouse ID'larini 1001+ ga o'tkazish
Bu Store va Warehouse ID conflict'ini hal qiladi
"""
from app import app, db, Warehouse, WarehouseStock, User, Transfer
from sqlalchemy import text

def migrate_warehouse_ids():
    with app.app_context():
        print("\n" + "="*80)
        print("WAREHOUSE ID MIGRATION")
        print("="*80)
        
        # 1. Mavjud warehouse'larni olish
        warehouses = Warehouse.query.order_by(Warehouse.id).all()
        print(f"\n📦 Found {len(warehouses)} warehouses")
        
        # Old ID -> New ID mapping
        id_mapping = {}
        new_id = 1001
        
        for warehouse in warehouses:
            id_mapping[warehouse.id] = new_id
            print(f"   Warehouse '{warehouse.name}': ID {warehouse.id} → {new_id}")
            new_id += 1
        
        if not id_mapping:
            print("\n⚠️ No warehouses found, nothing to migrate")
            return
        
        # 2. Yangi ID'lar bilan yangi warehouse'lar yaratish
        print(f"\n🔄 Step 1: Creating warehouses with new IDs...")
        
        for old_id, new_id in id_mapping.items():
            old_warehouse = Warehouse.query.get(old_id)
            
            # Check if new ID already exists
            existing = Warehouse.query.get(new_id)
            if existing:
                print(f"   ⚠️ Warehouse with ID={new_id} already exists, skipping")
                continue
            
            # Create new warehouse with new ID
            db.session.execute(text("""
                INSERT INTO warehouses (id, name, address, manager_name, phone, current_stock, created_at)
                VALUES (:new_id, :name, :address, :manager_name, :phone, :current_stock, :created_at)
            """), {
                'new_id': new_id,
                'name': old_warehouse.name,
                'address': old_warehouse.address,
                'manager_name': old_warehouse.manager_name,
                'phone': old_warehouse.phone,
                'current_stock': old_warehouse.current_stock,
                'created_at': old_warehouse.created_at
            })
            print(f"   ✅ Created warehouse ID={new_id} ({old_warehouse.name})")
        
        db.session.commit()
        
        # 3. Warehouse stock'larni yangilash
        print(f"\n🔄 Step 2: Updating warehouse_stock records...")
        for old_id, new_id in id_mapping.items():
            result = db.session.execute(text("""
                UPDATE warehouse_stock 
                SET warehouse_id = :new_id 
                WHERE warehouse_id = :old_id
            """), {'new_id': new_id, 'old_id': old_id})
            print(f"   ✅ Updated {result.rowcount} warehouse_stock records: {old_id} → {new_id}")
        
        db.session.commit()
        
        # 4. Transfer jadvalini yangilash (from_warehouse_id va to_warehouse_id)
        print(f"\n🔄 Step 3: Updating transfer records...")
        for old_id, new_id in id_mapping.items():
            # from_warehouse_id
            result1 = db.session.execute(text("""
                UPDATE transfers 
                SET from_warehouse_id = :new_id 
                WHERE from_warehouse_id = :old_id
            """), {'new_id': new_id, 'old_id': old_id})
            
            # to_warehouse_id
            result2 = db.session.execute(text("""
                UPDATE transfers 
                SET to_warehouse_id = :new_id 
                WHERE to_warehouse_id = :old_id
            """), {'new_id': new_id, 'old_id': old_id})
            
            total = result1.rowcount + result2.rowcount
            if total > 0:
                print(f"   ✅ Updated {total} transfer records: {old_id} → {new_id}")
        
        db.session.commit()
        
        # 5. User permissions'ni yangilash
        print(f"\n🔄 Step 4: Updating user permissions...")
        users = User.query.all()
        
        for user in users:
            updated = False
            
            # allowed_locations
            if user.allowed_locations:
                new_allowed = []
                for loc in user.allowed_locations:
                    if isinstance(loc, dict) and loc.get('type') == 'warehouse':
                        old_id = loc['id']
                        if old_id in id_mapping:
                            new_allowed.append({'id': id_mapping[old_id], 'type': 'warehouse'})
                            updated = True
                        else:
                            new_allowed.append(loc)
                    else:
                        new_allowed.append(loc)
                
                if updated:
                    user.allowed_locations = new_allowed
            
            # transfer_locations
            if user.transfer_locations:
                new_transfer = []
                for loc in user.transfer_locations:
                    if isinstance(loc, dict) and loc.get('type') == 'warehouse':
                        old_id = loc['id']
                        if old_id in id_mapping:
                            new_transfer.append({'id': id_mapping[old_id], 'type': 'warehouse'})
                            updated = True
                        else:
                            new_transfer.append(loc)
                    else:
                        new_transfer.append(loc)
                
                if updated:
                    user.transfer_locations = new_transfer
            
            if updated:
                print(f"   ✅ Updated user '{user.username}' permissions")
        
        db.session.commit()
        
        # 6. Eski warehouse'larni o'chirish
        print(f"\n🔄 Step 5: Deleting old warehouses...")
        for old_id in id_mapping.keys():
            db.session.execute(text("DELETE FROM warehouses WHERE id = :old_id"), {'old_id': old_id})
            print(f"   ✅ Deleted old warehouse ID={old_id}")
        
        db.session.commit()
        
        # 7. Auto-increment'ni yangi qiymatga o'rnatish
        print(f"\n🔄 Step 6: Setting auto-increment to {new_id}...")
        db.session.execute(text(f"ALTER SEQUENCE warehouses_id_seq RESTART WITH {new_id}"))
        db.session.commit()
        print(f"   ✅ Auto-increment set to {new_id}")
        
        print(f"\n{'='*80}")
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print(f"{'='*80}")
        print(f"\n💡 Warehouse IDs changed:")
        for old_id, new_id in id_mapping.items():
            print(f"   {old_id} → {new_id}")

if __name__ == '__main__':
    try:
        migrate_warehouse_ids()
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
