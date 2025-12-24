-- PostgreSQL connection va statement timeout sozlamalari
-- Database level'da sozlash

-- Statement timeout - 5 minut (uzun querylar uchun)
ALTER DATABASE dokon_db SET statement_timeout = '300s';

-- Idle in transaction timeout - 10 minut
ALTER DATABASE dokon_db SET idle_in_transaction_session_timeout = '600s';

-- Lock timeout - 30 sekund (deadlock oldini olish)
ALTER DATABASE dokon_db SET lock_timeout = '30s';

-- Tekshirish
SELECT name, setting, unit, short_desc
FROM pg_settings
WHERE name IN ('statement_timeout', 'idle_in_transaction_session_timeout', 'lock_timeout');
