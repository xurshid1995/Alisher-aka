from app import app, db, User, Store, Warehouse

with app.app_context():
    sotuvchi = User.query.filter_by(username='sotuvchi').first()
    
    print("\n" + "="*80)
    print("SOTUVCHI RUXSATLARI TAHLILI")
    print("="*80)
    
    print(f"\n👤 Username: {sotuvchi.username}")
    print(f"🎭 Role: {sotuvchi.role}")
    
    print(f"\n📍 allowed_locations ({len(sotuvchi.allowed_locations)} ta):")
    for i, loc in enumerate(sotuvchi.allowed_locations, 1):
        print(f"   {i}. {loc}")
    
    print(f"\n🔄 transfer_locations ({len(sotuvchi.transfer_locations)} ta):")
    for i, loc in enumerate(sotuvchi.transfer_locations, 1):
        print(f"   {i}. {loc}")
    
    print(f"\n✅ permissions:")
    print(f"   {sotuvchi.permissions}")
    
    # Takrorlanishlarni tekshirish
    print(f"\n🔍 MUAMMO TAHLILI:")
    print(f"   allowed_locations da takrorlanishlar:")
    
    location_ids = {}
    for loc in sotuvchi.allowed_locations:
        key = f"{loc['id']}_{loc['type']}"
        if key in location_ids:
            print(f"   ⚠️ TAKRORLANGAN: ID={loc['id']}, type={loc['type']}")
        else:
            location_ids[key] = loc
    
    # ID=1 ni tekshirish
    id_1_locations = [loc for loc in sotuvchi.allowed_locations if loc['id'] == 1]
    print(f"\n🔍 ID=1 bilan joylashuvlar ({len(id_1_locations)} ta):")
    for loc in id_1_locations:
        print(f"   - {loc}")
    
    # Ma'lumotlar bazasida ID=1 nima?
    store_1 = Store.query.get(1)
    warehouse_1 = Warehouse.query.get(1)
    
    print(f"\n📊 Ma'lumotlar bazasida ID=1:")
    if store_1:
        print(f"   Store: ID=1, Name={store_1.name}")
    if warehouse_1:
        print(f"   Warehouse: ID=1, Name={warehouse_1.name}")
    
    print(f"\n💡 XULOSA:")
    print(f"   Siz 2 ta joylashuv ruxsat bergansiz deyapsiz")
    print(f"   Lekin ma'lumotlar bazasida {len(sotuvchi.allowed_locations)} ta bor")
    print(f"   Sabab: ID=1 bir vaqtning o'zida Store va Warehouse'da mavjud!")
