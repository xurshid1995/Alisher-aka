"""
Check and recreate stores in the database.
"""

from app import app, db, Store
from sqlalchemy import text

def main():
    with app.app_context():
        print("\n" + "="*60)
        print("CHECKING STORES")
        print("="*60)
        
        stores = Store.query.all()
        print(f"\nTotal stores in database: {len(stores)}")
        
        if len(stores) == 0:
            print("\n⚠️ No stores found! Need to recreate.")
            print("\nRecreating store: Sergeli 1/4/3 with ID=1")
            
            # Create store with specific ID
            store = Store(
                id=1,
                name='Sergeli 1/4/3',
                address='Sergeli tumani, 1-mavze, 4-kvartal, 3-uy',
                manager_name='Manager',  # Required field
                phone='+998901234567'
            )
            
            db.session.add(store)
            db.session.commit()
            
            # Reset auto-increment to 2 (next store will get ID=2)
            db.session.execute(text("SELECT setval('stores_id_seq', 2, false)"))
            db.session.commit()
            
            print("✅ Store created successfully!")
            print(f"   - ID: {store.id}")
            print(f"   - Name: {store.name}")
            print(f"   - Auto-increment set to 2")
        else:
            print("\n✅ Stores exist:")
            for store in stores:
                print(f"   - ID={store.id}, Name={store.name}")

if __name__ == '__main__':
    main()
