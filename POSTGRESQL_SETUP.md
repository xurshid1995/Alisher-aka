# PostgreSQL O'rnatish Yo'riqnomasi

## Windows uchun PostgreSQL o'rnatish:

### 1. PostgreSQL yuklab olish:
- https://www.postgresql.org/download/windows/ sahifasiga o'ting
- "Download the installer" tugmasini bosing
- Eng so'nggi versiyani tanlang (PostgreSQL 15+ tavsiya etiladi)

### 2. O'rnatish jarayoni:
1. Yuklab olingan .exe faylni ishga tushiring
2. O'rnatish yo'lini tanlang (default qoldiring)
3. Komponentlarni tanlang (default qoldiring)
4. Ma'lumotlar katalogini tanlang (default qoldiring)
5. **Muhim**: Superuser (postgres) uchun parol o'rnating
   - Parolni eslab qoling! (masalan: "password")
6. Port: 5432 (default)
7. Locale: Default qoldiring
8. O'rnatishni yakunlang

### 3. PostgreSQL service tekshirish:
Quyidagi buyruqni PowerShell da bajaring:
```powershell
Get-Service postgresql*
```

Agar service ishlamasa:
```powershell
Start-Service postgresql-x64-15  # yoki sizning versiyangiz
```

### 4. PostgreSQL ulanishni tekshirish:

**A) psql orqali (Command line):**
```bash
psql -U postgres -h localhost
```
Parolni kiriting va ulanishni tekshiring.

**B) pgAdmin orqali (GUI):**
- Start menu'dan pgAdmin'ni oching
- Server qo'shing: localhost:5432
- Username: postgres
- Parol: o'rnatishda kiritgan parol

### 5. Ma'lumotlar bazasi yaratish:

**psql orqali:**
```sql
CREATE DATABASE sayt_db;
\l  -- barcha ma'lumotlar bazalarini ko'rish
\q  -- chiqish
```

**yoki Python script orqali:**
```bash
python create_postgres_db.py
```

### 6. .env faylini yangilash:
```env
DATABASE_URL=postgresql://postgres:SIZNING_PAROLINGIZ@localhost:5432/sayt_db
```

### 7. Keng tarqalgan muammolar:

**Muammo 1**: "psycopg2 topilmadi"
```bash
pip install psycopg2-binary
```

**Muammo 2**: "Connection refused"
- PostgreSQL service ishlab turganligini tekshiring
- Port 5432 bo'sh ekanligini tekshiring

**Muammo 3**: "Authentication failed"
- Username va parolni tekshiring
- pg_hba.conf faylini tekshiring

### 8. PostgreSQL'ni to'liq o'chirish (agar kerak bo'lsa):
1. Control Panel → Programs → Uninstall
2. PostgreSQL related barcha dasturlarni o'chiring
3. C:\Program Files\PostgreSQL papkasini o'chiring
4. C:\Users\USERNAME\AppData\Roaming\postgresql papkasini o'chiring

## PostgreSQL vs SQLite - Decimal qo'llab-quvvatlash:

### PostgreSQL (Tavsiya etiladi):
✅ DECIMAL va NUMERIC turlarini qo'llab-quvvatlaydi
✅ Aniq matematik hisoblashlar
✅ Katta precision va scale
✅ Enterprise loyihalar uchun

### SQLite:
❌ DECIMAL turini qo'llab-quvvatlamaydi
❌ Faqat TEXT, INTEGER, REAL, BLOB
❌ Decimal qiymatlar REAL (float) sifatida saqlanadi
❌ Aniqlik yo'qolishi mumkin

Bu loyihada PostgreSQL ishlatish shart, chunki Decimal ma'lumot turlarini to'g'ri namoyish qilish kerak!
