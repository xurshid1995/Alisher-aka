import psycopg2
import os

# Server DB
conn = psycopg2.connect(
    host='207.154.225.70',
    port=5432,
    database='sayt_db',
    user='postgres',
    password='postgres'
)
cur = conn.cursor()

cur.execute("""
    SELECT w.name,
           SUM(ws.quantity * p.cost_price)  AS jami_tan_narx,
           SUM(ws.quantity * p.sell_price)  AS jami_sotuv,
           SUM(ws.quantity)                 AS jami_miqdor
    FROM warehouse_stocks ws
    JOIN warehouses w ON ws.warehouse_id = w.id
    JOIN products p ON ws.product_id = p.id
    WHERE w.name ILIKE '%uy%'
    GROUP BY w.name
""")
rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"Ombor      : {row[0]}")
        print(f"Tan narx   : ${float(row[1]):,.2f}")
        print(f"Sotuv narx : ${float(row[2]):,.2f}")
        print(f"Miqdor     : {int(row[3]):,}")
        print()
else:
    print("'UY' nomli ombor topilmadi.")
    cur.execute("SELECT id, name FROM warehouses ORDER BY id")
    print("Mavjud omborlar:")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}")

cur.close()
conn.close()
