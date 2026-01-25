"""
Tasdiqlanmagan (pending) transferlar jadvalini yaratish
"""

from app import app, db
from sqlalchemy import text

def create_pending_transfers_table():
    """pending_transfers jadvalini yaratish"""
    with app.app_context():
        try:
            # Jadval mavjudligini tekshirish
            result = db.session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'pending_transfers'
                );
            """))
            exists = result.scalar()
            
            if exists:
                print("✅ pending_transfers jadvali allaqachon mavjud")
                return
            
            # Jadvalni yaratish
            db.session.execute(text("""
                CREATE TABLE pending_transfers (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    from_location_type VARCHAR(20) NOT NULL,
                    from_location_id INTEGER NOT NULL,
                    to_location_type VARCHAR(20) NOT NULL,
                    to_location_id INTEGER NOT NULL,
                    items JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Index yaratish
            db.session.execute(text("""
                CREATE INDEX idx_pending_transfers_user_id ON pending_transfers(user_id);
            """))
            
            # Trigger yaratish - updated_at ni avtomatik yangilash uchun
            db.session.execute(text("""
                CREATE OR REPLACE FUNCTION update_pending_transfers_updated_at()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """))
            
            db.session.execute(text("""
                CREATE TRIGGER trigger_update_pending_transfers_updated_at
                BEFORE UPDATE ON pending_transfers
                FOR EACH ROW
                EXECUTE FUNCTION update_pending_transfers_updated_at();
            """))
            
            db.session.commit()
            print("✅ pending_transfers jadvali muvaffaqiyatli yaratildi")
            print("✅ Index va trigger qo'shildi")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Xatolik: {str(e)}")
            raise

if __name__ == '__main__':
    create_pending_transfers_table()
