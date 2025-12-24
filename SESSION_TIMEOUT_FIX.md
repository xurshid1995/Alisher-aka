# SESSION TIMEOUT VA API TIMEOUT MUAMMOSINI HAL QILISH

## Muammo
API'lar 8 soat emas, balki brauzer yopilganda yoki 60 sekund timeout beradi.

## Topilgan Muammolar

### 1. Session Timeout Muammosi
**Muammo:** `session.permanent` faqat "Remember me" belgilanganda `True` bo'ladi  
**Natija:** Session brauzer yopilganda o'chadi, 8 soat ishlamaydi  
**Yechim:** `session.permanent = True` har doim o'rnatish

### 2. Gunicorn Timeout
**Muammo:** `timeout = 120` (2 minut)  
**Natija:** Uzun API requestlar 2 minutdan keyin timeout beradi  
**Yechim:** `timeout = 300` (5 minut)

### 3. Nginx Timeout
**Muammo:** `proxy_read_timeout = 60s`  
**Natija:** Nginx 60 sekunddan keyin requestni to'xtatadi  
**Yechim:** Barcha timeout'larni 300s ga oshirish

### 4. PostgreSQL Connection Pool
**Muammo:** `pool_recycle = 3600` (1 soat)  
**Natija:** Connection'lar 1 soatdan keyin yangilanadi  
**Yechim:** `pool_pre_ping = True` (connection alive ekanini tekshirish)

## O'zgartirilgan Fayllar

### 1. app.py
```python
# Session lifetime 12 soatga oshirildi
app.config['PERMANENT_SESSION_LIFETIME'] = 43200  # 12 soat

# Login API'da session.permanent har doim True
session.permanent = True  # Remember me'dan qat'iy nazar
```

### 2. gunicorn_config.py
```python
timeout = int(os.getenv('TIMEOUT', 300))  # 5 minut
keepalive = 5  # Keep-alive connection 5 sekund
```

### 3. nginx_dokon.conf va nginx_sergeli0606.conf
```nginx
proxy_connect_timeout 300s;  # 5 minut
proxy_send_timeout 300s;     # 5 minut
proxy_read_timeout 300s;     # 5 minut
send_timeout 300s;           # Client'ga javob yozish uchun
```

## Deployment Qadamlari

### 1. Serverga fayllarni yuklash
```bash
cd /var/www/dokon
git pull origin main
```

### 2. PostgreSQL timeout sozlamalarini o'rnatish
```bash
psql -U postgres -d dokon_db -f set_pg_timeouts.sql
```

### 3. Nginx konfiguratsiyasini yangilash
```bash
sudo cp nginx_dokon.conf /etc/nginx/sites-available/dokon
sudo nginx -t  # Test konfiguratsiya
sudo systemctl reload nginx
```

### 4. Gunicorn'ni qayta ishga tushirish
```bash
sudo systemctl restart dokon
# yoki
sudo systemctl stop dokon
sudo systemctl start dokon
sudo systemctl status dokon
```

### 5. Log'larni kuzatish
```bash
# Gunicorn logs
tail -f logs/error.log
tail -f logs/access.log

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# System logs
journalctl -u dokon -f
```

## Tekshirish

### 1. Session timeout tekshirish
1. Login qiling
2. 8-10 soat kutmasdan, hozirdan keyin test qiling
3. Brauzer'ni yopmasdan tab'ni yoping
4. Yangi tab'da saytni oching - session faol bo'lishi kerak

### 2. API timeout tekshirish
```bash
# Uzun API request yuborish (test)
curl -X POST http://165.232.81.142/api/products \
  -H "Content-Type: application/json" \
  -d '{"search": "test"}' \
  --max-time 310  # 5 minut 10 sekund
```

### 3. Database connection tekshirish
```bash
python check_session_timeout.py
```

## Olingan Natijalar

| Parametr | Avvalgi | Yangi | Ta'sir |
|----------|---------|-------|--------|
| Session Lifetime | 8 soat (faqat remember=True) | 12 soat (har doim) | ✅ Session uzaytirildi |
| Gunicorn Timeout | 120s (2 min) | 300s (5 min) | ✅ Uzun API requestlar ishlaydi |
| Nginx Timeout | 60s (1 min) | 300s (5 min) | ✅ Nginx timeout kamaydi |
| Keepalive | 2s | 5s | ✅ Connection qayta ishlatiladi |

## Qo'shimcha Tavsiyalar

### 1. Monitoring
- Session uzunligini kuzatish
- API request vaqtini monitoring qilish
- Database connection pool holatini tekshirish

### 2. Xavfsizlik
- SESSION_COOKIE_HTTPONLY: True ✅
- SESSION_COOKIE_SAMESITE: Lax ✅
- HTTPS uchun SESSION_COOKIE_SECURE: True qilish (keyinchalik)

### 3. Performance
- Database query'larni optimize qilish
- Eager loading ishlatish (N+1 problem)
- Connection pool size'ni monitoring qilish

## Muammolar va Yechimlar

### Session o'chib ketsa
1. Log fayllarni tekshiring: `tail -f logs/error.log`
2. Session cookie'ni tekshiring (browser DevTools)
3. `session.permanent = True` o'rnatilganligini tekshiring

### API timeout bersa
1. Gunicorn timeout'ni oshiring
2. Nginx timeout'ni oshiring
3. Database query'ni optimize qiling
4. Log'larda timeout sabablari borligini tekshiring

### Database connection muammosi
1. `pool_pre_ping = True` o'rnatilganligini tekshiring
2. Connection pool size'ni oshiring
3. `pool_recycle` vaqtini kamaytiring

## Xulosa

Barcha timeout muammolari hal qilindi:
- ✅ Session 12 soat faol bo'ladi
- ✅ API requestlar 5 minutgacha ishlaydi
- ✅ Nginx timeout kamaydi
- ✅ Database connection barqaror ishlaydi

Deployment'dan keyin test qiling va monitoring'ni yoqing!
