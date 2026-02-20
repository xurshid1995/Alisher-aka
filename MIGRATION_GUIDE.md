# Server'da migration ishga tushirish uchun qo'llanma

## SSH orqali serverga ulanish:
```bash
ssh root@46.101.153.212
```

## Migration ishga tushirish:
```bash
cd /var/www/jamshid

# Python virtual environment'ni activate qilish
source venv/bin/activate

# Migration faylini ishga tushirish
python3 run_stock_check_items_migration.py
```

## Yoki to'g'ridan-to'g'ri SQL fayl orqali:
```bash
sudo -u postgres psql dokon_baza < migrations/create_stock_check_items_table.sql
```

## Jadval yaratilganini tekshirish:
```bash
sudo -u postgres psql dokon_baza -c "\d stock_check_items"
```

## Gunicorn restart qilish:
```bash
sudo systemctl restart jamshid
```
