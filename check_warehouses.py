from app import app, Warehouse

with app.app_context():
    warehouses = Warehouse.query.all()
    print(f"Total warehouses: {len(warehouses)}")
    for w in warehouses:
        print(f"  ID={w.id}, Name={w.name}")
