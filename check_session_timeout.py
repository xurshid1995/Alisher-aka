"""
Session timeout va database timezone muammolarini tekshirish
"""
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import psycopg2
import urllib.parse

# Environment variables yuklash
load_dotenv()

# Database ulanish parametrlari
db_params = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'sayt_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

print("=" * 60)
print("SESSION TIMEOUT VA TIMEZONE TEKSHIRISH")
print("=" * 60)
print()

# 1. App.py'dagi session konfiguratsiyasini ko'rsatish
print("1. SESSION KONFIGURATSIYASI (app.py):")
print(f"   - PERMANENT_SESSION_LIFETIME: 28800 sekund (8 soat)")
print(f"   - SESSION_COOKIE_HTTPONLY: True")
print(f"   - SESSION_COOKIE_SAMESITE: Lax")
print(f"   - session.permanent: Faqat remember=True bo'lganda")
print()

# 2. Database connection pool konfiguratsiyasi
print("2. DATABASE CONNECTION POOL:")
print(f"   - pool_size: 10")
print(f"   - pool_recycle: 3600 sekund (1 soat)")
print(f"   - pool_timeout: 30 sekund")
print(f"   - connect_timeout: 10 sekund")
print()

try:
    # Database'ga ulanish
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    print("3. DATABASE TIMEZONE:")
    print("-" * 60)
    
    # Server timezone
    cursor.execute("SHOW timezone;")
    db_timezone = cursor.fetchone()[0]
    print(f"   Database timezone: {db_timezone}")
    
    # Current timestamp
    cursor.execute("SELECT NOW(), CURRENT_TIMESTAMP;")
    now, timestamp = cursor.fetchone()
    print(f"   Database NOW(): {now}")
    print(f"   Database CURRENT_TIMESTAMP: {timestamp}")
    
    # Python timezone
    python_now = datetime.now()
    python_utc_now = datetime.now(timezone.utc)
    print(f"   Python NOW() (local): {python_now}")
    print(f"   Python NOW() (UTC): {python_utc_now}")
    print()
    
    # 4. Eng oxirgi sale'larning vaqtini tekshirish
    print("4. ENG OXIRGI SALE'LAR:")
    print("-" * 60)
    cursor.execute("""
        SELECT id, sale_date, created_at, 
               EXTRACT(EPOCH FROM (NOW() - sale_date)) / 3600 as hours_ago
        FROM sales 
        ORDER BY id DESC 
        LIMIT 5;
    """)
    
    sales = cursor.fetchall()
    if sales:
        for sale in sales:
            sale_id, sale_date, created_at, hours_ago = sale
            print(f"   Sale #{sale_id}:")
            print(f"      - sale_date: {sale_date}")
            print(f"      - created_at: {created_at}")
            print(f"      - Hours ago: {hours_ago:.2f}")
            print()
    else:
        print("   Sale'lar topilmadi")
    
    # 5. Session timeout muammosini aniqlash
    print("5. MUAMMO TAHLILI:")
    print("-" * 60)
    
    if db_timezone.upper() != 'ASIA/TASHKENT':
        print("   ⚠️  MUAMMO TOPILDI!")
        print(f"   Database timezone: {db_timezone}")
        print(f"   Kerakli timezone: Asia/Tashkent")
        print()
        print("   Bu muammo quyidagicha ta'sir qiladi:")
        print("   - Sale'lar UTC vaqtda saqlanadi")
        print("   - Lekin foydalanuvchi O'zbekiston vaqtida ishlaydi")
        print("   - 8 soat farq paydo bo'ladi (UTC+5)")
        print()
        print("   YECHIM:")
        print("   1. Database timezone'ni o'zgartirish:")
        print(f"      ALTER DATABASE {db_params['database']} SET timezone TO 'Asia/Tashkent';")
        print()
    else:
        print("   ✅ Database timezone to'g'ri: Asia/Tashkent")
        print()
    
    # Session timeout muammosi
    print("   SESSION TIMEOUT MUAMMOSI:")
    print("   - PERMANENT_SESSION_LIFETIME = 28800 sek (8 soat)")
    print("   - Lekin session.permanent faqat remember=True bo'lganda o'rnatiladi")
    print("   - Agar remember=False bo'lsa, session brauzer yopilganda o'chadi")
    print()
    print("   YECHIM:")
    print("   1. login API'da session.permanent = True qilish (doim)")
    print("   2. Yoki PERMANENT_SESSION_LIFETIME ni 24 soatga oshirish")
    print()
    
    cursor.close()
    conn.close()
    
    print("=" * 60)
    print("XULOSA:")
    print("=" * 60)
    print("Muammo: Session timeout 8 soat emas, balki brauzer yopilganda o'chadi")
    print("Sabab: session.permanent faqat 'remember me' belgilanganda True bo'ladi")
    print()
    print("Tavsiya:")
    print("1. session.permanent = True ni har doim o'rnatish")
    print("2. Database timezone'ni Asia/Tashkent ga o'zgartirish")
    print("=" * 60)

except Exception as e:
    print(f"❌ Xatolik: {e}")
    import traceback
    traceback.print_exc()
