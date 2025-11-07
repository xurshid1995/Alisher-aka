# PostgreSQL parol tuzatish yo'riqnomasi

## Keng tarqalgan default parollar:
1. postgres
2. password
3. admin
4. 123456
5. root
6. (bo'sh parol)

## .env faylida har birini sinab ko'ring:

# 1-variant:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sayt_db

# 2-variant:
DATABASE_URL=postgresql://postgres:password@localhost:5432/sayt_db

# 3-variant:
DATABASE_URL=postgresql://postgres:admin@localhost:5432/sayt_db

# 4-variant:
DATABASE_URL=postgresql://postgres:123456@localhost:5432/sayt_db

# 5-variant (bo'sh parol):
DATABASE_URL=postgresql://postgres@localhost:5432/sayt_db

## Agar hech biri ishlamasa:

### Windows'da PostgreSQL parolini tiklash:

1. PostgreSQL service'ni to'xtatish:
   ```
   Stop-Service postgresql-x64-17
   ```

2. pg_hba.conf faylini topish:
   ```
   C:\Program Files\PostgreSQL\17\data\pg_hba.conf
   ```

3. Faylni tahrirlash (notepad yoki VS Code'da):
   - Quyidagi qatorni toping:
   ```
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   host    all             all             127.0.0.1/32            scram-sha-256
   ```
   
   - `scram-sha-256` ni `trust` ga o'zgartiring:
   ```
   host    all             all             127.0.0.1/32            trust
   ```

4. Service'ni qayta ishga tushirish:
   ```
   Start-Service postgresql-x64-17
   ```

5. Parol o'rnatish:
   ```
   psql -U postgres -c "ALTER USER postgres PASSWORD 'yangi_parol';"
   ```

6. pg_hba.conf'ni qaytarish:
   ```
   host    all             all             127.0.0.1/32            scram-sha-256
   ```

7. Service'ni qayta ishga tushirish:
   ```
   Restart-Service postgresql-x64-17
   ```

## Eng oson yechim:
PostgreSQL'ni o'chirib, qayta o'rnatish va o'rnatish jarayonida parolni eslab qolish.
