# Fix /\.?0+$/ regex bug in debts.html
# Read as bytes to avoid encoding issues, work with encoded strings

with open('templates/debts.html', 'rb') as f:
    raw = f.read()

fixes = [
    # All instances of .toFixed(5).replace(/\.?0+$/, "")
    # Replace with parseFloat(...toFixed(5)).toString() pattern
    # We do text substitutions on the utf-8 decoded string then re-encode
]

content = raw.decode('utf-8-sig')  # handles BOM if present

replacements = [
    ('sale.debt_usd.toFixed(5).replace(/\\.?0+$/, "")', 'parseFloat(sale.debt_usd.toFixed(5)).toString()'),
    ('noDateTotal.toFixed(5).replace(/\\.?0+$/, "")', 'parseFloat(noDateTotal.toFixed(5)).toString()'),
    ('remainingDebt.toFixed(5).replace(/\\.?0+$/, "")', 'parseFloat(remainingDebt.toFixed(5)).toString()'),
    ('lastPaymentAmount.toFixed(5).replace(/\\.?0+$/, "")', 'parseFloat(lastPaymentAmount.toFixed(5)).toString()'),
    ('sale.debt_usd.toFixed(5).replace(/\\.?0+$/, "")', 'parseFloat(sale.debt_usd.toFixed(5)).toString()'),
    ('debtAmount.toFixed(5).replace(/\\.?0+$/, "")', 'parseFloat(debtAmount.toFixed(5)).toString()'),
]

for old, new in replacements:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f'Replaced {count}x: {old[:50]}')

# Re-encode without BOM
out = content.encode('utf-8')
with open('templates/debts.html', 'wb') as f:
    f.write(out)
print('Done')
