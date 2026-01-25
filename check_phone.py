#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, db, Customer

with app.app_context():
    # Xurshid mijozni topish (ID=16)
    customer = Customer.query.get(16)
    
    if customer:
        print(f"\n✅ Mijoz topildi:")
        print(f"   ID: {customer.id}")
        print(f"   Name: {customer.name}")
        print(f"   Phone: [{customer.phone}]")
        print(f"   Telegram Chat ID: {customer.telegram_chat_id}")
        print(f"   Telegram Chat ID mavjudmi: {'✅ HA' if customer.telegram_chat_id else '❌ YO\'Q'}")
    else:
        print("\n❌ Mijoz topilmadi")

