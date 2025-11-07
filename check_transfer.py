from app import app, db, User

# Transfer locations bor foydalanuvchilarni tekshirish
with app.app_context():
    users = User.query.filter(User.role != 'admin').limit(5).all()

    for user in users:
        print(f"\n{'=' * 60}")
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Role: {user.role}")
        print(f"Allowed locations: {user.allowed_locations}")
        print(f"Transfer locations: {user.transfer_locations}")
        print(f"Permissions: {user.permissions}")
