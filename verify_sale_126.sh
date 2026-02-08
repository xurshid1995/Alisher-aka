#!/bin/bash

export PGPASSWORD='bwjtaUueHturzUv2TuNf'

echo "========================================="
echo "   SALE 126 - TO'LIQ TEKSHIRUV"
echo "========================================="
echo ""

psql -h localhost -U xurshid_user -d xurshid_db << 'EOF'

\pset border 2
\pset format wrapped

SELECT 
    '🛒 SAVDO MA''LUMOTLARI' as "INFO";

SELECT 
    s.id as "ID",
    TO_CHAR(s.created_at, 'DD.MM.YYYY HH24:MI:SS') as "Vaqt",
    s.total_amount as "Jami $",
    s.cash_usd as "To''lov $",
    s.cash_amount as "To''lov so''m",
    CASE 
        WHEN s.total_amount = s.cash_usd THEN '✅ TO''G''RI'
        ELSE '❌ XATO'
    END as "Status"
FROM sales s
WHERE s.id = 126;

SELECT '' as "";
SELECT '📦 SAVDO MAHSULOTLARI' as "INFO";

SELECT 
    ROW_NUMBER() OVER (ORDER BY si.id) as "№",
    si.id as "Item ID",
    p.name as "Mahsulot",
    si.quantity as "Soni",
    si.unit_price as "Narx $",
    si.total_price as "Jami $"
FROM sale_items si
JOIN products p ON si.product_id = p.id
WHERE si.sale_id = 126
ORDER BY si.id;

SELECT '' as "";
SELECT '📊 HISOB' as "INFO";

SELECT 
    SUM(si.total_price) as "Items jami $",
    s.total_amount as "Sale total $",
    CASE 
        WHEN SUM(si.total_price) = s.total_amount THEN '✅ MOS'
        ELSE '❌ MOS EMAS'
    END as "Status"
FROM sale_items si, sales s
WHERE si.sale_id = 126 AND s.id = 126
GROUP BY s.total_amount;

SELECT '' as "";
SELECT '📦 STOCK HOLATI (Teyes Q8)' as "INFO";

SELECT 
    ss.id as "Stock ID",
    p.name as "Mahsulot",
    ss.quantity as "Qoldiq",
    st.name as "Ombor"
FROM store_stocks ss
JOIN products p ON ss.product_id = p.id
JOIN stores st ON ss.store_id = st.id
WHERE ss.product_id = 144;

EOF

echo ""
echo "========================================="
echo "   ✅ TEKSHIRUV YAKUNLANDI"
echo "========================================="
