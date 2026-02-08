#!/bin/bash

export PGPASSWORD='bwjtaUueHturzUv2TuNf'

echo "========================================="
echo "   TIMEOUT MUAMMOLARINI TEKSHIRISH"
echo "========================================="
echo ""

echo "=== 1. PostgreSQL Timeout Settings ==="
psql -h localhost -U xurshid_user -d xurshid_db << 'EOF'
SELECT 
    name,
    setting,
    unit,
    CASE 
        WHEN name = 'idle_in_transaction_session_timeout' THEN 
            CASE 
                WHEN setting::int = 0 THEN 'Cheksiz (yaxshi)'
                WHEN setting::int < 60000 THEN 'Juda qisqa! (1 minutdan kam)'
                ELSE 'OK'
            END
        WHEN name = 'statement_timeout' THEN 
            CASE 
                WHEN setting::int = 0 THEN 'Cheksiz'
                WHEN setting::int < 10000 THEN 'Juda qisqa! (10 sekunddan kam)'
                ELSE 'OK'
            END
        ELSE ''
    END as status
FROM pg_settings
WHERE name IN (
    'idle_in_transaction_session_timeout',
    'statement_timeout',
    'lock_timeout',
    'max_connections'
)
ORDER BY name;
EOF

echo ""
echo "=== 2. Aktiv Database Connections ==="
psql -h localhost -U xurshid_user -d xurshid_db << 'EOF'
SELECT 
    state,
    COUNT(*) as count,
    MAX(EXTRACT(EPOCH FROM (NOW() - state_change))) as max_age_seconds
FROM pg_stat_activity
WHERE datname = 'xurshid_db'
GROUP BY state
ORDER BY count DESC;
EOF

echo ""
echo "=== 3. Uzoq Vaqt Idle Bo'lgan Connections ==="
psql -h localhost -U xurshid_user -d xurshid_db << 'EOF'
SELECT 
    pid,
    usename,
    application_name,
    state,
    EXTRACT(EPOCH FROM (NOW() - state_change)) as idle_seconds,
    query
FROM pg_stat_activity
WHERE datname = 'xurshid_db'
  AND state = 'idle'
  AND state_change < NOW() - INTERVAL '5 minutes'
ORDER BY state_change
LIMIT 10;
EOF

echo ""
echo "=== 4. Database Locks (Deadlock muammolari) ==="
psql -h localhost -U xurshid_user -d xurshid_db << 'EOF'
SELECT 
    COUNT(*) as lock_count,
    mode
FROM pg_locks
WHERE database = (SELECT oid FROM pg_database WHERE datname = 'xurshid_db')
GROUP BY mode
ORDER BY lock_count DESC;
EOF

echo ""
echo "========================================="
echo "   TEKSHIRUV YAKUNLANDI"
echo "========================================="
