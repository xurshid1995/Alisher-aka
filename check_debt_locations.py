#!/usr/bin/env python3
"""Qarz savdolarning location ma'lumotlarini tekshirish"""
from app import app, db, Sale

with app.app_context():
    # Qarz savdolarni olish
    debt_sales = Sale.query.filter_by(payment_status='partial').order_by(Sale.id.desc()).limit(10).all()
    
    print(f"\n📊 Jami qarz savdolar: {Sale.query.filter_by(payment_status='partial').count()}")
    print(f"\n🔍 Oxirgi 10 ta qarz savdo:\n")
    
    for sale in debt_sales:
        print(f"ID: {sale.id:4d} | Location: {sale.location_id or 'NULL':4} | Type: {sale.location_type or 'NULL':10} | Amount: ${sale.total_amount:7.2f} | Date: {sale.sale_date}")
    
    # Har xil location_id'lar
    print(f"\n📍 Qarz savdolardagi unique location_id va type:")
    unique_locations = db.session.query(Sale.location_id, Sale.location_type).filter_by(payment_status='partial').distinct().all()
    for loc_id, loc_type in unique_locations:
        count = Sale.query.filter_by(payment_status='partial', location_id=loc_id, location_type=loc_type).count()
        print(f"   Location ID: {loc_id or 'NULL':4} | Type: {loc_type or 'NULL':10} | Count: {count}")
