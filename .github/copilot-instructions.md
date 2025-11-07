<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Python Web Application with PostgreSQL

Bu loyiha Python Flask framework va PostgreSQL ma'lumotlar bazasi yordamida yaratilgan web ilovadir.

## Asosiy komponentlar:
- **Backend**: Flask web framework
- **Database**: PostgreSQL 
- **Frontend**: HTML, CSS, JavaScript (Jinja2 templating)
- **ORM**: SQLAlchemy

## Decimal ma'lumotlar bilan ishlash:
- PostgreSQL DECIMAL/NUMERIC turlaridan foydalaning
- Python'da decimal.Decimal moduli bilan ishlang
- SQLAlchemy'da DECIMAL turi uchun precision va scale ko'rsating

## Kodlash standartlari:
- PEP 8 Python kod uslubiga rioya qiling
- Barcha ma'lumotlar bazasi operatsiyalarida transaction ishlatish
- Error handling va logging qo'shing
- Ma'lumotlarni validatsiya qilish
