with open(r'templates/sales.html', 'rb') as f:
    c = f.read()
i = c.find(b'closeScannerBtn')
# Find closing quote + > after Yopish
chunk = c[i:i+600]
j = chunk.find(b'Yopish">')
if j >= 0:
    print("Found:", chunk[j:j+20])
else:
    # try without double quote
    j = chunk.find(b'Yopish')
    print("Yopish at:", j, "bytes:", chunk[j:j+25])
