-- Transfer jadvalidagi product_id foreign key ga CASCADE qo'shish
-- Bu Product o'chirilganda unga tegishli transferlar ham o'chirilishini ta'minlaydi

-- Avval eski constraint ni o'chirish
ALTER TABLE transfers DROP CONSTRAINT IF EXISTS transfers_product_id_fkey;

-- Yangi constraint CASCADE bilan qo'shish
ALTER TABLE transfers 
ADD CONSTRAINT transfers_product_id_fkey 
FOREIGN KEY (product_id) 
REFERENCES products(id) 
ON DELETE CASCADE;
