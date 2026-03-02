-- Hosting mijozlarga status_token ustuni qo'shish
ALTER TABLE hosting_clients
ADD COLUMN IF NOT EXISTS status_token VARCHAR(64) UNIQUE;

-- Har bir mijozga random token yaratish
UPDATE hosting_clients
SET status_token = md5(random()::text || id::text || now()::text)
WHERE status_token IS NULL;
