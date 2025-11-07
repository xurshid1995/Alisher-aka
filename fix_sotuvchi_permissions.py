"""
Fix sotuvchi permissions after warehouse ID migration.
Update to use correct warehouse ID (1002 for Akfa).
"""
from app import app, db, User

with app.app_context():
    sotuvchi = User.query.filter_by(username='sotuvchi').first()
    
    if not sotuvchi:
        print("❌ sotuvchi user not found!")
        exit(1)
    
    print("\n" + "="*60)
    print("FIXING SOTUVCHI PERMISSIONS")
    print("="*60)
    
    print(f"\n📍 Current allowed_locations ({len(sotuvchi.allowed_locations)} ta):")
    for loc in sotuvchi.allowed_locations:
        print(f"   - ID={loc['id']}, Type={loc['type']}")
    
    # New correct locations:
    # - Store ID=1 (Sergeli 1/4/3)
    # - Warehouse ID=1002 (Akfa - new ID after migration)
    new_allowed_locations = [
        {'id': 1, 'type': 'store'},
        {'id': 1002, 'type': 'warehouse'}
    ]
    
    print(f"\n📍 New allowed_locations ({len(new_allowed_locations)} ta):")
    for loc in new_allowed_locations:
        print(f"   - ID={loc['id']}, Type={loc['type']}")
    
    # Update transfer_locations as well
    new_transfer_locations = [
        {'id': 1, 'type': 'store'},
        {'id': 1002, 'type': 'warehouse'}
    ]
    
    print(f"\n🔄 New transfer_locations ({len(new_transfer_locations)} ta):")
    for loc in new_transfer_locations:
        print(f"   - ID={loc['id']}, Type={loc['type']}")
    
    # Save changes
    sotuvchi.allowed_locations = new_allowed_locations
    sotuvchi.transfer_locations = new_transfer_locations
    
    try:
        db.session.commit()
        print(f"\n✅ Changes saved successfully!")
        print(f"\n💡 sotuvchi will now see exactly 2 locations:")
        print(f"   1. Sergeli 1/4/3 (Store - ID=1)")
        print(f"   2. Akfa (Warehouse - ID=1002)")
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {str(e)}")
