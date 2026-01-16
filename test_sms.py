# -*- coding: utf-8 -*-
"""
ESKIZ.UZ SMS xizmatini test qilish
"""
from sms_eskiz import eskiz_sms

def test_balance():
    """Balansni tekshirish"""
    print("\n" + "="*60)
    print("💰 SMS BALANSNI TEKSHIRISH")
    print("="*60)
    
    balance = eskiz_sms.get_balance()
    if balance:
        print(f"✅ Balans ma'lumotlari:")
        print(f"   📊 Limit: {balance.get('limit', 'N/A')}")
        print(f"   📈 Is limit: {balance.get('is_limit', 'N/A')}")
    else:
        print("❌ Balansni olishda xatolik")
        print("⚠️  .env faylda ESKIZ_EMAIL va ESKIZ_PASSWORD to'g'ri kiritilganmi tekshiring")

def test_send_sms():
    """Oddiy SMS yuborish"""
    print("\n" + "="*60)
    print("📱 TEST SMS YUBORISH")
    print("="*60)
    
    # Telefon raqam so'rash
    phone = input("📞 Telefon raqam (998901234567 yoki 901234567): ").strip()
    
    if not phone:
        print("❌ Telefon raqam kiritilmadi")
        return
    
    message = "Salom! Bu ESKIZ.UZ dan test SMS. Agar bu xabar kelgan bo'lsa, integratsiya muvaffaqiyatli!"
    
    print(f"\n📤 SMS yuborilmoqda...")
    print(f"   📞 Raqam: {phone}")
    print(f"   💬 Xabar: {message}")
    
    result = eskiz_sms.send_sms(phone, message)
    
    print("\n" + "-"*60)
    if result['success']:
        print(f"✅ SMS muvaffaqiyatli yuborildi!")
        print(f"   🆔 Message ID: {result.get('message_id')}")
        print(f"   📱 Jo'natilgan raqam: {result.get('phone')}")
        print(f"   ⏰ 1-2 daqiqada SMS kelishi kerak")
    else:
        print(f"❌ Xatolik yuz berdi: {result['error']}")

def test_debt_reminder():
    """Qarz eslatmasi test"""
    print("\n" + "="*60)
    print("💰 QARZ ESLATMASI SMS TEST")
    print("="*60)
    
    phone = input("📞 Mijoz telefoni (998901234567): ").strip()
    if not phone:
        print("❌ Telefon kiritilmadi")
        return
    
    name = input("👤 Mijoz ismi: ").strip() or "Mijoz"
    
    try:
        debt = float(input("💵 Qarz miqdori (USD, masalan 50.00): ").strip() or 100)
    except ValueError:
        print("❌ Noto'g'ri summa kiritildi")
        return
    
    print(f"\n📤 Qarz eslatmasi yuborilmoqda...")
    result = eskiz_sms.send_debt_reminder(phone, name, debt)
    
    print("\n" + "-"*60)
    if result['success']:
        print("✅ Qarz eslatmasi yuborildi!")
        print(f"   🆔 Message ID: {result.get('message_id')}")
    else:
        print(f"❌ Xatolik: {result['error']}")

def test_payment_confirmation():
    """To'lov tasdiqlanishi test"""
    print("\n" + "="*60)
    print("✅ TO'LOV TASDIQLANISHI SMS TEST")
    print("="*60)
    
    phone = input("📞 Mijoz telefoni (998901234567): ").strip()
    if not phone:
        print("❌ Telefon kiritilmadi")
        return
    
    name = input("👤 Mijoz ismi: ").strip() or "Mijoz"
    
    try:
        paid = float(input("💵 To'langan summa (USD): ").strip() or 50)
        remaining = float(input("💰 Qolgan qarz (USD, 0 = to'liq to'langan): ").strip() or 0)
    except ValueError:
        print("❌ Noto'g'ri summa kiritildi")
        return
    
    print(f"\n📤 To'lov tasdiqlanishi yuborilmoqda...")
    result = eskiz_sms.send_payment_confirmation(phone, name, paid, remaining)
    
    print("\n" + "-"*60)
    if result['success']:
        print("✅ To'lov tasdiqlanishi yuborildi!")
        print(f"   🆔 Message ID: {result.get('message_id')}")
    else:
        print(f"❌ Xatolik: {result['error']}")

def main():
    """Asosiy menyu"""
    print("\n" + "="*60)
    print("🎯 ESKIZ.UZ SMS XIZMATI TEST")
    print("="*60)
    print("📍 Diqqat: .env faylda ESKIZ_EMAIL va ESKIZ_PASSWORD sozlangan bo'lishi kerak!")
    print("="*60)
    
    while True:
        print("\n📋 MENYU:")
        print("1️⃣  SMS Balansni tekshirish")
        print("2️⃣  Oddiy SMS yuborish")
        print("3️⃣  Qarz eslatmasi yuborish")
        print("4️⃣  To'lov tasdiqlanishi yuborish")
        print("0️⃣  Chiqish")
        
        choice = input("\n👉 Tanlang (0-4): ").strip()
        
        if choice == '1':
            test_balance()
        elif choice == '2':
            test_send_sms()
        elif choice == '3':
            test_debt_reminder()
        elif choice == '4':
            test_payment_confirmation()
        elif choice == '0':
            print("\n👋 Xayr! SMS xizmati integratsiyasi muvaffaqiyatli!")
            break
        else:
            print("❌ Noto'g'ri tanlov. Iltimos 0-4 oralig'ida kiriting.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Dastur to'xtatildi")
    except Exception as e:
        print(f"\n❌ Xatolik: {str(e)}")
