# 🐛 Qoldiq Tekshirish - Auto-Save Debug Guide

## 📊 Console'da qanday ma'lumotlar ko'rinadi:

### 1️⃣ **Modal oynada miqdor kiritish:**
```
⌨️ [09:45:23.456] Modal input o'zgardi: "5"
🔄 [09:45:23.457] AUTO-SAVE chaqirildi
   ⏹️ Oldingi timer bekor qilindi
💾 [09:45:23.457] ✅ Saqlash BOSHLANDI
📦 [09:45:23.458] savePageState() boshlandi
   📍 Joylashuv: store_1
   🔄 Tekshiruv faol: true
   📦 Mahsulotlar: 150 ta
   ✅ Tekshirilgan: 5 ta
   💾 localStorage'ga saqlandi (8432 bytes)
   🌐 Server'ga yuborish rejalashtirildi
✅ [09:45:23.460] savePageState() tugadi
✅ [09:45:23.460] Saqlash TUGADI
```

### 2️⃣ **"Saqlash" tugmasi bosilganda:**
```
💾 [09:45:30.123] ========== SAQLASH TUGMASI BOSILDI ==========
   📦 Mahsulot: Pepsi 1.5L (ID: 42)
   🔢 Asl miqdor: 10
   🔢 Yangi miqdor: 8
   ✅ Server javob berdi
   🚪 Modal oyna yopildi
   🔄 Mavjud mahsulot yangilandi
   🔄 AutoSave chaqirilmoqda...
🔄 [09:45:30.145] AUTO-SAVE chaqirildi
💾 [09:45:30.145] ✅ Saqlash BOSHLANDI
📦 [09:45:30.146] savePageState() boshlandi
   📍 Joylashuv: store_1
   🔄 Tekshiruv faol: true
   📦 Mahsulotlar: 149 ta
   ✅ Tekshirilgan: 6 ta
   💾 localStorage'ga saqlandi (8956 bytes)
   🌐 Server'ga yuborish rejalashtirildi
✅ [09:45:30.148] savePageState() tugadi
✅ [09:45:30.148] Saqlash TUGADI
========== SAQLASH JARAYONI TUGADI ==========
```

### 3️⃣ **Immediate Save (muhim amallar):**
```
⚡ [09:45:45.789] IMMEDIATE SAVE chaqirildi
   ⏹️ saveTimeout bekor qilindi
   ⏹️ serverSaveTimeout bekor qilindi
   💾 LocalStorage'ga saqlandi
   🌐 Server'ga yuborildi
✅ [09:45:45.790] IMMEDIATE SAVE tugadi
```

## 🎯 Nimalarni kuzatish mumkin:

1. **⏱️ Vaqt:** Har bir operatsiya millisoniyalar bilan
2. **📍 Joylashuv:** Qaysi do'kon/omborda ishlayapsiz
3. **📦 Mahsulotlar soni:** Nechta mahsulot qolgan
4. **✅ Tekshirilgan:** Nechta mahsulot tekshirilgan
5. **💾 Hajm:** Qancha ma'lumot saqlanmoqda (bytes)
6. **🌐 Server:** Server'ga yuborilish holati

## 🔍 Debug qanday ishlatish:

### Chrome DevTools'da:
1. **F12** bosing yoki **Right Click → Inspect**
2. **Console** tab'ini oching
3. Qoldiq tekshirish sahifasiga o'ting
4. Mahsulot tanlang va miqdor kiriting
5. Console'da barcha operatsiyalar ko'rinadi

### Filtr qilish:
```javascript
// Faqat AUTO-SAVE'ni ko'rish
🔄

// Faqat SAQLASH tugmasini ko'rish
💾 [.*] ==========

// Faqat xatoliklarni ko'rish
❌
```

## 📈 Performance tahlili:

### Yaxshi natija:
- AUTO-SAVE: 0-5ms
- savePageState(): 2-10ms
- Server yuborish: 10-50ms

### Muammo belgisi:
- AUTO-SAVE: >50ms ⚠️
- savePageState(): >100ms ⚠️
- Server yuborish: >500ms ⚠️

## 💡 Foydali maslahatlar:

1. **Console'ni tozalash:** `clear()` yoki `Ctrl+L`
2. **Copy qilish:** Right click → Copy object
3. **Timestamp filter:** `[09:45:*]` qidiruv
4. **Export:** Right click → Save as...

## 🔧 Debug o'chirish:

Agar console'ni tozalamoqchi bo'lsangiz, barcha `console.log` qatorlarini comment qiling yoki o'chiring.

---
**Yaratildi:** 2025-11-07
**Maqsad:** Auto-save jarayonini real-time kuzatish
