# Python Web Sayt - PostgreSQL va Decimal

Bu loyiha Python Flask framework va PostgreSQL ma'lumotlar bazasi yordamida yaratilgan web ilovadir. Loyihada Decimal ma'lumot turi bilan ishlash ko'rsatilgan.

## 🚀 Loyiha haqida

### Texnologiyalar:
- **Backend**: Python Flask
- **Database**: PostgreSQL  
- **Frontend**: HTML, CSS, JavaScript
- **ORM**: SQLAlchemy
- **Ma'lumot turlari**: Decimal (aniq matematik hisoblashlar uchun)

## 📊 Decimal vs Float

### Decimal qulayliklari:
✅ **Aniq matematik hisoblashlar** - pul operatsiyalari uchun ideal
✅ **Yaxlitlash nazorati** - aniq precision va scale
✅ **PostgreSQL mos keladi** - DECIMAL/NUMERIC turlari bilan
✅ **Xatoliklar yo'q** - 0.1 + 0.2 = 0.3 (aniq natija)

### Decimal kamchiliklari:
❌ **Sekinroq** - float ga nisbatan
❌ **Ko'proq xotira** - har bir qiymat uchun
❌ **JSON muammolari** - to'g'ridan-to'g'ri serialize bo'lmaydi
❌ **Cheklangan matematik funksiyalar** - ba'zi operatsiyalar qo'llab-quvvatlanmaydi

## 🛠 O'rnatish

### 1. Python virtual environment yaratish:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# yoki
source venv/bin/activate  # Linux/Mac
```

### 2. Kerakli paketlarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 3. PostgreSQL o'rnatish va konfiguratsiya:
```bash
# PostgreSQL o'rnatish (Windows)
# https://www.postgresql.org/download/windows/

# Ma'lumotlar bazasi yaratish
createdb sayt_db
```

### 4. Environment variables o'rnatish:
`.env` faylini tahrirlang:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/sayt_db
SECRET_KEY=your-very-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🏃‍♂️ Ishga tushirish

```bash
python app.py
```

Brauzerda ochish: `http://localhost:5000`

## 📁 Loyiha strukturasi

```
d:\Sayt 2025\
├── app.py                 # Asosiy Flask aplikatsiya
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── .github/
│   └── copilot-instructions.md
├── templates/
│   ├── index.html        # Bosh sahifa
│   └── add_product.html  # Mahsulot qo'shish
├── static/
│   ├── css/
│   │   └── style.css     # CSS stillar
│   └── js/
│       └── main.js       # JavaScript funksiyalar
└── README.md
```

## 🔧 API Endpoints

### GET `/`
Bosh sahifa - mahsulotlar ro'yxati

### GET/POST `/add_product`
Yangi mahsulot qo'shish sahifasi

### GET `/api/products`
JSON formatda mahsulotlar ro'yxati

### POST `/api/products`
API orqali yangi mahsulot qo'shish

### GET `/api/calculate`
Decimal hisoblash misoli - jami qiymat

## 💾 Ma'lumotlar bazasi modellari

### Product (Mahsulot)
```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)
    description = db.Column(db.Text)
    stock_quantity = db.Column(db.Integer, default=0)
```

### Order (Buyurtma)
```python
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.DECIMAL(precision=12, scale=2), nullable=False)
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
```

## 🧮 Decimal ishlatish misollari

### Python'da Decimal yaratish:
```python
from decimal import Decimal

# To'g'ri usul
price = Decimal('1500000.99')

# Noto'g'ri (float dan)
price = Decimal(1500000.99)  # Aniqlik yo'qolishi mumkin
```

### PostgreSQL'da Decimal:
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL  -- 10 raqam, 2 ta kasr
);
```

### SQLAlchemy'da Decimal:
```python
price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)
```

## 🎯 Foydalanish misollari

1. **Mahsulot qo'shish**: `/add_product` sahifasiga o'ting
2. **API orqali**: JavaScript `addProductViaAPI()` funksiyasidan foydalaning
3. **Jami hisoblash**: "Jami qiymat" tugmasini bosing
4. **Aniqlik ko'rsatish**: Browser console'da decimal vs float farqini ko'ring

## 🔍 Test qilish

Browser console'da:
```javascript
// Decimal aniqlikni ko'rsatish
demonstrateDecimalPrecision();

// API orqali mahsulot qo'shish
addProductViaAPI({
    name: "Test mahsulot",
    price: 999999.99,
    description: "Test tavsif",
    stock_quantity: 5
});
```

## 📝 Qo'shimcha eslatmalar

- Barcha pul miqdorlari uchun Decimal ishlatilgan
- PostgreSQL DECIMAL turi bilan mos keladi  
- JSON API'da float ga aylantiriladi (frontend uchun)
- Xatoliklar va validatsiya qo'shilgan
- Modern responsive UI dizayni

## 🤝 Hissa qo'shish

1. Loyihani fork qiling
2. Yangi branch yarating
3. O'zgarishlarni commit qiling
4. Pull request yuboring

## 📄 Litsenziya

MIT License

---

**Muallif:** Python Web Developer  
**Sana:** September 2025  
**Maqsad:** Decimal ma'lumot turlari bilan ishlashni o'rgatish
