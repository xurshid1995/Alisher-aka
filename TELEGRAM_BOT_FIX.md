# 🔧 Telegram Bot Muammolarini Hal Qilish

## ✅ Amalga oshirilgan tuzatishlar

### 1. **Telefon raqam tasdiqlash tizimi yaxshilandi**
   - Telefon raqam contact orqali yoki matn sifatida yuborilishi mumkin
   - Tasdiqlash kodi yanada aniq ko'rsatmalar bilan yuboriladi
   - Debugging loglar qo'shildi

### 2. **Tugmalar (Qarzni tekshirish va To'lov tarixi)**
   - Start buyrug'ida mijoz allaqachon ro'yxatdan o'tgan bo'lsa, darhol tugmalar ko'rsatiladi
   - Tasdiqlash kodini kiritgandan so'ng tugmalar avtomatik ko'rsatiladi

### 3. **Xatoliklar aniq ko'rsatiladi**
   - Agar mijoz topilmasa, aniq xabar beriladi
   - Tasdiqlash kodi noto'g'ri bo'lsa, qayta urinish imkoni beriladi

## 📋 Botni ishga tushirish uchun qadamlar

### 1. `.env` faylini sozlash

`.env.example` faylidan nusxa oling va `.env` nomi bilan saqlang:

```bash
cp .env.example .env
```

Keyin `.env` faylini tahrirlang va quyidagilarni to'ldiring:

#### a) Telegram Bot Token olish:
1. Telegram'da **@BotFather** ni qidiring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username kiriting
4. BotFather sizga **token** beradi (masalan: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Bu tokenni `.env` faylidagi `TELEGRAM_BOT_TOKEN` ga kiriting

#### b) Admin Chat ID olish:
1. Telegram'da **@userinfobot** ni qidiring
2. `/start` yuboring
3. Bot sizga **chat ID** beradi (masalan: `123456789`)
4. Bu ID ni `.env` faylidagi `TELEGRAM_ADMIN_CHAT_IDS` ga kiriting

### 2. Botni ishga tushirish

#### Usul 1: Run Telegram Bot faylidan
```bash
python run_telegram_bot.py
```

#### Usul 2: Systemd service sifatida (Linux)
```bash
# Service faylini ko'chirish
sudo cp telegram-bot.service /etc/systemd/system/

# Service'ni ishga tushirish
sudo systemctl daemon-reload
sudo systemctl start telegram-bot
sudo systemctl enable telegram-bot

# Status tekshirish
sudo systemctl status telegram-bot
```

#### Usul 3: Flask app bilan birgalikda
Flask app avval ishga tushirilishi kerak, keyin bot avtomatik ishga tushadi.

### 3. Botni tekshirish

1. Telegram'da botingizni qidiring (masalan: `@Sergeli143_bot`)
2. `/start` buyrug'ini yuboring
3. "📱 Telefon raqamni yuborish" tugmasini bosing yoki telefon raqamni matn sifatida yuboring (masalan: `+998901234567`)
4. Bot sizga 6 raqamli tasdiqlash kodini yuboradi
5. Kodni ko'chirib oling va botga yuboring
6. Muvaffaqiyatli tasdiqlangandan so'ng, "💰 Qarzni tekshirish" va "📜 To'lov tarixi" tugmalari paydo bo'ladi

## 🐛 Muammolarni bartaraf etish

### Muammo 1: "Tasdiqlash kodi kelmayapti"

**Sabablari:**
- Bot ishlamayapti
- TELEGRAM_BOT_TOKEN noto'g'ri yoki yo'q
- Mijoz telefon raqami database'da yo'q yoki noto'g'ri formatda

**Yechim:**
1. Botning ishlab turganligini tekshiring:
   ```bash
   # Loglarni ko'rish
   tail -f logs/telegram_bot.log
   
   # Yoki systemd service bo'lsa
   sudo journalctl -u telegram-bot -f
   ```

2. `.env` faylida `TELEGRAM_BOT_TOKEN` to'g'ri kiritilganligini tekshiring

3. Database'da mijoz telefon raqami to'g'ri saqlanganligini tekshiring:
   ```sql
   SELECT id, name, phone FROM customers WHERE phone LIKE '%901234567%';
   ```

### Muammo 2: "Tugmalar ko'rinmayapti"

**Sabablari:**
- Mijoz tasdiqlash kodini noto'g'ri kiritgan
- Bot qayta ishga tushgan va verification_codes xotiradan o'chgan

**Yechim:**
1. Mijoz tasdiqlash kodini to'g'ri kiritganligini tekshiring (6 raqamli kod)
2. Agar kod yo'qolgan bo'lsa, `/start` dan qayta boshlang
3. Mijoz allaqachon ro'yxatdan o'tgan bo'lsa, `/start` ni qayta yuborganida tugmalar avtomatik ko'rsatiladi

### Muammo 3: "Mijoz topilmadi"

**Sabablari:**
- Telefon raqam database'da noto'g'ri formatda saqlangan
- Mijoz hali yaratilmagan

**Yechim:**
1. Database'da telefon raqamlarni tekshiring:
   ```sql
   SELECT id, name, phone FROM customers ORDER BY id DESC LIMIT 10;
   ```

2. Telefon raqam formatini to'g'rilash:
   ```sql
   -- Agar telefon raqamlar noto'g'ri formatda bo'lsa
   UPDATE customers SET phone = '+998' || TRIM(phone) WHERE phone NOT LIKE '+998%';
   ```

3. Yangi mijoz qo'shish uchun Flask app'dan foydalaning

## 📝 Loglarni tekshirish

Bot ishlashini kuzatish uchun loglarni tekshiring:

```bash
# Telegram bot loglari
tail -f logs/telegram_bot.log

# Flask app loglari
tail -f logs/app.log

# Sistemd service loglari (agar service sifatida ishga tushirilgan bo'lsa)
sudo journalctl -u telegram-bot -f
```

## 🔍 Debugging

Kod ichida ko'plab debugging loglar qo'shilgan:

- `📱 Contact qabul qilindi` - kontakt qabul qilindi
- `🔍 Telefon qidirish` - telefon raqam qidirilmoqda
- `✅ Mijoz topildi` - mijoz topildi
- `🔐 Tasdiqlash kodi yaratildi` - tasdiqlash kodi yaratildi
- `➡️ Tasdiqlash kodi yuborildi` - tasdiqlash kodi yuborildi
- `📥 Kiritilgan kod` - mijoz kod kiritdi
- `✅ Tasdiqlash kodi to'g'ri` - tasdiqlash muvaffaqiyatli

Bu loglarni kuzatib, muammoning qayerda ekanligini aniqlash mumkin.

## 🎯 Keyingi qadamlar

1. `.env` faylini sozlang
2. Botni ishga tushiring
3. Telegram'da `/start` dan boshlang
4. Telefon raqamni yuboring (contact yoki matn)
5. Tasdiqlash kodini kiriting
6. Tugmalardan foydalaning

Agar muammolar davom etsa, loglarni tekshiring yoki admin bilan bog'laning.
