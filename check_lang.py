#!/usr/bin/env python3
"""Til sozlamalarini tekshirish - diagnostika skripti"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from app import db, app, Settings

with app.app_context():
    # User language settings
    langs = Settings.query.filter(Settings.key.like('user_language_%')).all()
    print("=== Foydalanuvchi til sozlamalari ===")
    for l in langs:
        print(f"  {l.key} = {l.value}")
    if not langs:
        print("  (hech narsa topilmadi)")

    # Global language setting
    g = Settings.query.filter_by(key='language').first()
    print(f"\n=== Global til sozlamasi ===")
    print(f"  language = {g.value if g else '(NOT SET)'}")

    # All settings
    print(f"\n=== Barcha sozlamalar ===")
    all_settings = Settings.query.all()
    for s in all_settings:
        print(f"  {s.key} = {s.value}")
