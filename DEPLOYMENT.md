# Digital Ocean Deployment Guide

## 1. Server sozlash

```bash
# Server yangilash
sudo apt update && sudo apt upgrade -y

# Python va kerakli paketlar
sudo apt install python3 python3-pip python3-venv postgresql nginx -y
```

## 2. PostgreSQL sozlash

```bash
# PostgreSQL ga kirish
sudo -u postgres psql

# Database yaratish
CREATE DATABASE sayt_db;
CREATE USER your_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE sayt_db TO your_user;
\q
```

## 3. Loyihani yuklash

```bash
# Loyiha papkasini yaratish
mkdir -p /var/www/sayt2025
cd /var/www/sayt2025

# Git clone (yoki fayllarni yuklash)
# git clone your-repo-url .

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Dependencies o'rnatish
pip install -r requirements.txt
```

## 4. Environment sozlash

```bash
# .env faylini yaratish
cp .env.production.example .env

# .env faylini tahrirlash
nano .env
```

**Muhim**: `.env` da SECRET_KEY va DB_PASSWORD ni o'zgartiring!

```bash
# Strong SECRET_KEY generatsiya qilish
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 5. Logs papkasini yaratish

```bash
mkdir -p logs
chmod 755 logs
```

## 6. Gunicorn systemd service

```bash
sudo nano /etc/systemd/system/sayt2025.service
```

```ini
[Unit]
Description=Sayt 2025 Gunicorn Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sayt2025
Environment="PATH=/var/www/sayt2025/venv/bin"
ExecStart=/var/www/sayt2025/venv/bin/gunicorn -c gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Service ni yoqish
sudo systemctl daemon-reload
sudo systemctl start sayt2025
sudo systemctl enable sayt2025
sudo systemctl status sayt2025
```

## 7. Nginx sozlash

```bash
sudo nano /etc/nginx/sites-available/sayt2025
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/sayt2025/static;
        expires 30d;
    }
}
```

```bash
# Nginx sozlamasini yoqish
sudo ln -s /etc/nginx/sites-available/sayt2025 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 8. SSL (Let's Encrypt)

```bash
# Certbot o'rnatish
sudo apt install certbot python3-certbot-nginx -y

# SSL sertifikat olish
sudo certbot --nginx -d your-domain.com
```

## 9. Firewall

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

## 10. Log monitoring

```bash
# Application logs
tail -f logs/error.log
tail -f logs/access.log

# Systemd logs
sudo journalctl -u sayt2025 -f
```

## Restart commands

```bash
# Application restart
sudo systemctl restart sayt2025

# Nginx restart
sudo systemctl restart nginx

# Database restart
sudo systemctl restart postgresql
```

## Backup

```bash
# Database backup
pg_dump -U your_user sayt_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U your_user sayt_db < backup_20231107.sql
```

## Troubleshooting

### Service ishlamasa:
```bash
sudo systemctl status sayt2025
sudo journalctl -u sayt2025 -n 50
```

### Database connection muammosi:
```bash
# PostgreSQL holatini tekshirish
sudo systemctl status postgresql

# Connection test
psql -U your_user -d sayt_db -h localhost
```

### Permission muammolari:
```bash
sudo chown -R www-data:www-data /var/www/sayt2025
sudo chmod -R 755 /var/www/sayt2025
```
