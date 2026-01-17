#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Sessions jadvali yaratish migratsiyasi
"""

from app import app, db
from sqlalchemy import text

def create_user_sessions_table():
    """user_sessions jadvalini yaratish"""
    
    with app.app_context():
        try:
            print("🔄 user_sessions jadvali yaratilmoqda...")
            
            # Jadvalni yaratish
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS user_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                session_id VARCHAR(255) NOT NULL UNIQUE,
                login_time TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tashkent'),
                last_activity TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tashkent'),
                ip_address VARCHAR(45),
                user_agent TEXT,
                is_active BOOLEAN DEFAULT TRUE NOT NULL,
                created_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tashkent')
            );
            """
            
            db.session.execute(text(create_table_sql))
            
            # Indexlar yaratish
            print("🔄 Indexlar yaratilmoqda...")
            
            index_queries = [
                "CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);",
                "CREATE INDEX IF NOT EXISTS idx_user_sessions_session_id ON user_sessions(session_id);",
                "CREATE INDEX IF NOT EXISTS idx_user_sessions_is_active ON user_sessions(is_active);",
                "CREATE INDEX IF NOT EXISTS idx_user_sessions_login_time ON user_sessions(login_time);"
            ]
            
            for query in index_queries:
                db.session.execute(text(query))
            
            db.session.commit()
            
            print("✅ user_sessions jadvali va indexlar muvaffaqiyatli yaratildi!")
            
            # Jadvalni tekshirish
            check_sql = "SELECT COUNT(*) as count FROM user_sessions;"
            result = db.session.execute(text(check_sql))
            count = result.fetchone()[0]
            print(f"📊 user_sessions jadvalida {count} ta yozuv mavjud")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Xatolik: {e}")
            raise

if __name__ == '__main__':
    create_user_sessions_table()
