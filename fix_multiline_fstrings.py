import re

# app.py faylini o'qish
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Multi-line f-stringlarni topish va tuzatish
# Pattern: f"... { \n ... }"
pattern = r'f"([^"]*)\{\s*\n\s*([^}]+)\}'

def fix_fstring(match):
    prefix = match.group(1)
    inner = match.group(2).strip().replace('\n', ' ').replace('  ', ' ')
    return f'f"{prefix}{{{inner}}}'

# Tuzatish
fixed_content = content
prev_content = None

# Bir necha marta ishlatish (nested case lar uchun)
while prev_content != fixed_content:
    prev_content = fixed_content
    fixed_content = re.sub(pattern, fix_fstring, fixed_content, flags=re.MULTILINE)

# Saqlash
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Multi-line f-strings fixed!")
