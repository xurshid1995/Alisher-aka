UPDATE settings SET value = '@SMShisobot_bot' WHERE key = 'telegram_bot_name';
UPDATE settings SET value = 'https://t.me/SMShisobot_bot' WHERE key = 'telegram_bot_link';
SELECT key, value FROM settings WHERE key LIKE 'telegram%';
