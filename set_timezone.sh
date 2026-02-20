#!/bin/bash
# Server va Database vaqtini Asia/Tashkent ga o'zgartirish

echo "=== 1. Server timezone o'zgartirilmoqda ==="
timedatectl set-timezone Asia/Tashkent
echo "Server vaqti: $(date)"

echo ""
echo "=== 2. PostgreSQL timezone o'zgartirilmoqda ==="
sudo -u postgres psql -c "ALTER SYSTEM SET timezone TO 'Asia/Tashkent';"
sudo -u postgres psql -d alisher_aka_db -c "ALTER DATABASE alisher_aka_db SET timezone TO 'Asia/Tashkent';"
systemctl restart postgresql
sleep 2

echo ""
echo "=== 3. Flask .env ga timezone qo'shilmoqda ==="
grep -q "TZ=" /var/www/alisher-aka/.env && \
    sed -i 's/TZ=.*/TZ=Asia\/Tashkent/' /var/www/alisher-aka/.env || \
    echo "TZ=Asia/Tashkent" >> /var/www/alisher-aka/.env

echo ""
echo "=== 4. Servis restart ==="
systemctl restart alisher-aka

echo ""
echo "=== NATIJA ==="
echo "Server vaqti: $(date)"
timedatectl | grep "Time zone"
echo ""
echo "PostgreSQL timezone:"
sudo -u postgres psql -c "SHOW timezone;"
echo ""
echo "PostgreSQL hozirgi vaqt:"
sudo -u postgres psql -c "SELECT NOW();"
