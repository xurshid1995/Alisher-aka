"""Patch sales.html:
1. Add camera permission modal after the scanner modal closing tag
2. Replace alert() with styled modal in startBarcodeScanner()
"""

with open(r'templates/sales.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1. Add cameraPermissionModal after barcodeScannerModal ──────────────
camera_modal = '''
<!-- Kamera ruxsat yo\'riqnomasi modali -->
<div id="cameraPermissionModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.75); z-index:99999; align-items:center; justify-content:center;">
    <div style="background:#fff; border-radius:16px; padding:28px 24px; max-width:380px; width:90%; margin:auto; box-shadow:0 8px 40px rgba(0,0,0,0.3);">
        <div style="text-align:center; margin-bottom:16px;"><span style="font-size:48px;">📷</span></div>
        <h3 style="margin:0 0 12px; color:#dc3545; text-align:center; font-size:18px;">Kameraga ruxsat kerak</h3>
        <p style="margin:0 0 16px; color:#555; font-size:14px; line-height:1.6;">Brauzer kameraga kirishni bloklagan. Ruxsat berish uchun:</p>
        <div style="background:#f8f9fa; border-radius:10px; padding:14px; margin-bottom:16px; font-size:13px; color:#333; line-height:2;" id="cameraPermSteps"></div>
        <div style="display:flex; gap:10px;">
            <button onclick="document.getElementById(\'cameraPermissionModal\').style.display=\'none\'" style="flex:1; padding:10px; border:1px solid #ccc; background:#fff; border-radius:8px; cursor:pointer; font-size:14px;">Yopish</button>
            <button onclick="location.reload()" style="flex:1; padding:10px; background:#28a745; color:\'#fff\'; border:none; border-radius:8px; cursor:pointer; font-size:14px; font-weight:600;">🔄 Yangilash</button>
        </div>
    </div>
</div>
'''

# Insert after the closing </div> of barcodeScannerModal then the blank line
# The modal ends with: </div>\n\n<!-- Scanner uslublari -->
marker = '</div>\n\n<!-- Scanner uslublari -->'
if camera_modal.strip() in content:
    print("Camera modal already present, skipping step 1")
elif marker in content:
    content = content.replace(marker, '</div>\n' + camera_modal + '\n<!-- Scanner uslublari -->', 1)
    print("Step 1 OK: camera modal added")
else:
    print("ERROR: could not find marker for step 1")
    print("Searching for nearby text...")
    idx = content.find('Scanner uslublari')
    print(repr(content[idx-100:idx+30]))

# ─── 2. Replace alert(msg) + stopBarcodeScanner + return with modal ──────
old_alert = '''            alert(msg);
            stopBarcodeScanner();
            return;'''

new_modal = '''                // Styled modal ko\'rsatish
                const permModal = document.getElementById('cameraPermissionModal');
                const permSteps = document.getElementById('cameraPermSteps');
                if (permSteps) {
                    const isIOS = /iPhone|iPad|iPod/.test(navigator.userAgent);
                    const isChrome = /Chrome/.test(navigator.userAgent) && !/Edg/.test(navigator.userAgent);
                    const isSamsung = /SamsungBrowser/.test(navigator.userAgent);
                    if (isIOS) {
                        permSteps.innerHTML = '1️⃣ <b>iPhone Sozlamalar</b> → <b>Safari</b> → <b>Kamera</b><br>2️⃣ <b>sergeli0606.uz</b> ni toping → <b>Ruxsat</b> ni tanlang<br>3️⃣ Sahifani yangilang';
                    } else if (isSamsung) {
                        permSteps.innerHTML = '1️⃣ Brauzer <b>⋮ menyu</b> → <b>Sozlamalar</b> → <b>Sayt sozlamalari</b> → <b>Kamera</b><br>2️⃣ <b>sergeli0606.uz</b> ni toping → <b>Ruxsat</b> ni tanlang<br>3️⃣ Sahifani yangilang';
                    } else if (isChrome) {
                        permSteps.innerHTML = '1️⃣ Manzil qatoridagi 🔒 belgisini bosing<br>2️⃣ <b>Kamera</b> → <b>Har doim ruxsat berish</b> ni tanlang<br>3️⃣ <b>Sahifani yangilang</b> tugmasini bosing';
                    } else {
                        permSteps.innerHTML = '1️⃣ Brauzer manzil qatoridagi kamera belgisini bosing<br>2️⃣ <b>Ruxsat berish</b> ni tanlang<br>3️⃣ Sahifani yangilang';
                    }
                }
                if (permModal) permModal.style.display = 'flex';
                stopBarcodeScanner();
                return;'''

if old_alert in content:
    content = content.replace(old_alert, new_modal, 1)
    print("Step 2 OK: alert replaced with modal")
else:
    print("ERROR: could not find alert pattern for step 2")
    idx = content.find('alert(msg)')
    if idx >= 0:
        print(repr(content[idx-100:idx+100]))
    else:
        print("alert(msg) not found either")

with open(r'templates/sales.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. File saved.")
