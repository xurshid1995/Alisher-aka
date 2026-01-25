#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qaytarilgan mahsulotlar tarixini o'chirish
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2

# Environment variables yuklash
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'sayt_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

try:
    # Database'ga ulanish
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    # Avval nechta yozuv borligini tekshirish
    cursor.execute("SELECT COUNT(*) FROM operations_history WHERE operation_type='return';")
    count_before = cursor.fetchone()[0]
    print(f"📊 Tozalashdan oldin: {count_before} ta yozuv")
    
    if count_before == 0:
        print("✅ O'chiriladigan yozuv yo'q!")
        sys.exit(0)
    
    # Tasdiqlash
    confirm = input(f"⚠️  {count_before} ta yozuvni o'chirmoqchimisiz? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Bekor qilindi")
        sys.exit(0)
    
    # O'chirish
    cursor.execute("DELETE FROM operations_history WHERE operation_type='return';")
    conn.commit()
    
    # Natijani tekshirish
    cursor.execute("SELECT COUNT(*) FROM operations_history WHERE operation_type='return';")
    count_after = cursor.fetchone()[0]
    
    deleted_count = count_before - count_after
    print(f"✅ {deleted_count} ta yozuv o'chirildi!")
    print(f"📊 Qolgan yozuvlar: {count_after}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Xatolik: {str(e)}")
    sys.exit(1)
