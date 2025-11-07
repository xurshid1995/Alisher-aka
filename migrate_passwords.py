#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database migration script - parollarni hash qilish
Eski parollarni bcrypt bilan hash qilingan parollarga o'zgartiradi
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import after path is set  # noqa: E402
from app import app, db, User, hash_password

def migrate_passwords():
    """Barcha user parollarini hash qilish"""
    with app.app_context():
        try:
            print("🔄 Parollarni hash qilish boshlanmoqda...")
            
            users = User.query.all()
            updated_count = 0
            
            for user in users:
                # Agar parol allaqachon hash qilingan bo'lsa (bcrypt format)
                if user.password.startswith('$2b$'):
                    print(f"✓ {user.username} allaqachon hash qilingan")
                    continue
                
                # Parolni hash qilish
                old_password = user.password
                user.password = hash_password(old_password)
                updated_count += 1
                print(f"✓ {user.username} paroli hash qilindi")
            
            db.session.commit()
            print(f"\n✅ {updated_count} ta user paroli yangilandi")
            print(f"📊 Jami userlar: {len(users)}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Xatolik: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    print("⚠️  OGOHLANTIRISH: Bu script barcha user parollarini hash qiladi.")
    print("⚠️  Backup olinganligiga ishonch hosil qiling!")
    print()
    
    response = input("Davom etishni xohlaysizmi? (yes/no): ")
    if response.lower() == 'yes':
        migrate_passwords()
    else:
        print("❌ Bekor qilindi")
