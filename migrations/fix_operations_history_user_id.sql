-- OperationHistory jadvalidagi user_id foreign key constraint'ini o'zgartirish
-- Foydalanuvchi o'chirilganda user_id NULL bo'lishi kerak (username saqlanadi)

-- 1. Eski constraint'ni o'chirish
ALTER TABLE operations_history 
DROP CONSTRAINT IF EXISTS operations_history_user_id_fkey;

-- 2. user_id ustunini nullable qilish
ALTER TABLE operations_history 
ALTER COLUMN user_id DROP NOT NULL;

-- 3. Yangi constraint qo'shish (SET NULL bilan)
ALTER TABLE operations_history 
ADD CONSTRAINT operations_history_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;
