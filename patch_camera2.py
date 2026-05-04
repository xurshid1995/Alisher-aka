"""Patch sales.html - Step 2 only: replace alert(msg) with styled modal."""

with open(r'templates/sales.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_alert = '            alert(msg);\n            stopBarcodeScanner();\n            return;'

new_modal = (
    '            // Styled modal ko\'rsatish\n'
    '            const permModal = document.getElementById(\'cameraPermissionModal\');\n'
    '            const permSteps = document.getElementById(\'cameraPermSteps\');\n'
    '            if (permSteps) {\n'
    '                const isIOS = /iPhone|iPad|iPod/.test(navigator.userAgent);\n'
    '                const isChrome = /Chrome/.test(navigator.userAgent) && !/Edg/.test(navigator.userAgent);\n'
    '                const isSamsung = /SamsungBrowser/.test(navigator.userAgent);\n'
    '                if (isIOS) {\n'
    '                    permSteps.innerHTML = \'1. <b>iPhone Sozlamalar</b> → <b>Safari</b> → <b>Kamera</b><br>2. <b>sergeli0606.uz</b> → <b>Ruxsat</b><br>3. Sahifani yangilang\';\n'
    '                } else if (isSamsung) {\n'
    '                    permSteps.innerHTML = \'1. Brauzer <b>⋮ menyu</b> → <b>Sozlamalar</b> → <b>Sayt sozlamalari</b> → <b>Kamera</b><br>2. <b>sergeli0606.uz</b> → <b>Ruxsat</b><br>3. Sahifani yangilang\';\n'
    '                } else if (isChrome) {\n'
    '                    permSteps.innerHTML = \'1. Manzil qatoridagi 🔒 belgisini bosing<br>2. <b>Kamera</b> → <b>Har doim ruxsat berish</b><br>3. Sahifani yangilang tugmasini bosing\';\n'
    '                } else {\n'
    '                    permSteps.innerHTML = \'Brauzer manzil qatoridagi kamera belgisini bosib, <b>Ruxsat berish</b> ni tanlang va sahifani yangilang\';\n'
    '                }\n'
    '            }\n'
    '            if (permModal) permModal.style.display = \'flex\';\n'
    '            stopBarcodeScanner();\n'
    '            return;'
)

if old_alert in content:
    content = content.replace(old_alert, new_modal, 1)
    print("Step 2 OK: alert replaced with modal")
    with open(r'templates/sales.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("File saved.")
else:
    print("ERROR: pattern not found")
    idx = content.find('alert(msg)')
    if idx >= 0:
        print(repr(content[idx-5:idx+60]))
