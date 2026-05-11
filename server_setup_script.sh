#!/bin/bash
set -e

echo "======================================"
echo "  ALISHER SERVER SETUP"
echo "======================================"

# 1. PostgreSQL
echo "[1/5] PostgreSQL sozlanmoqda..."
systemctl start postgresql
systemctl enable postgresql

sudo -u postgres psql <<EOF
CREATE DATABASE alisher_db;
EOF
sudo -u postgres psql <<EOF
CREATE USER alisher_user WITH PASSWORD 'teleport7799';
ALTER ROLE alisher_user SET client_encoding TO 'utf8';
ALTER ROLE alisher_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE alisher_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE alisher_db TO alisher_user;
EOF
sudo -u postgres psql -d alisher_db <<EOF
GRANT ALL ON SCHEMA public TO alisher_user;
EOF
echo "  PostgreSQL OK"

# 2. Loyihani clone qilish
echo "[2/5] Loyiha clone qilinmoqda..."
mkdir -p /var/www/alisher
cd /var/www/alisher
if [ -d ".git" ]; then
    git pull origin main
else
    git clone https://github.com/xurshid1995/Alisher-aka.git .
fi
echo "  Git OK"

# 3. Virtual environment
echo "[3/5] Python venv sozlanmoqda..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -q
pip install gunicorn -q
echo "  Python venv OK"

# 4. .env fayl yaratish
echo "[4/5] .env fayl yaratilmoqda..."
SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
cat > /var/www/alisher/.env <<ENVEOF
DB_HOST=localhost
DB_PORT=5432
DB_NAME=alisher_db
DB_USER=alisher_user
DB_PASSWORD=teleport7799
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=${SECRET}
DEFAULT_PHONE_PLACEHOLDER=Telefon kiritilmagan
ENVEOF
echo "  .env OK"

# 5. Log papkasi
mkdir -p /var/www/alisher/logs
chmod 755 /var/www/alisher/logs

# 6. Systemd service
echo "[5/5] Systemd service yaratilmoqda..."
cat > /etc/systemd/system/alisher.service <<SVCEOF
[Unit]
Description=Alisher Flask App
After=network.target postgresql.service

[Service]
User=root
Group=root
WorkingDirectory=/var/www/alisher
Environment="PATH=/var/www/alisher/venv/bin"
EnvironmentFile=/var/www/alisher/.env
ExecStart=/var/www/alisher/venv/bin/gunicorn -c gunicorn_config.py app:app
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=alisher

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable alisher.service
systemctl start alisher.service
sleep 3
systemctl status alisher.service --no-pager -n 10
echo "  Service OK"

# 7. Nginx sozlash
echo "Nginx sozlanmoqda..."
cp /var/www/alisher/nginx_allonavto.conf /etc/nginx/sites-available/alisher
# HTTP only config (SSL keyinchalik)
cat > /etc/nginx/sites-available/alisher <<NGINXEOF
server {
    listen 80;
    listen [::]:80;
    server_name 207.154.225.70 www.allonavto.uz 207.154.225.70;

    client_max_body_size 10M;

    location /static {
        alias /var/www/alisher/static;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
NGINXEOF

ln -sf /etc/nginx/sites-available/alisher /etc/nginx/sites-enabled/alisher
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx && systemctl enable nginx
echo "  Nginx OK"

echo ""
echo "======================================"
echo "  SETUP MUVAFFAQIYATLI TUGADI!"
echo "  https://www.allonavto.uz"
echo "======================================"
