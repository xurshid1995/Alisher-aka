#!/bin/bash
echo "Qarz savdolar location ma'lumotlari:"
sudo -u postgres psql sayt_db -c "SELECT id, location_id, location_type, payment_status FROM sales WHERE payment_status='partial' ORDER BY id DESC LIMIT 10;"
