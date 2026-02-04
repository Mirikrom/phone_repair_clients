# Telefon Ustaxonasi - Klentlar bilan ishlash tizimi

Django va Django template bilan yozilgan telefon ta'mirlash ustaxonasi uchun klentlar boshqaruv tizimi.

## O'rnatish

```bash
# Virtual muhit yaratish
python -m venv venv

# Virtual muhitni faollashtirish
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Django o'rnatish
pip install Django

# Migratsiyalarni qo'llash
python manage.py migrate

# Superuser yaratish (admin panel uchun, ixtiyoriy)
python manage.py createsuperuser
```

## Ishga tushirish

```bash
python manage.py runserver
```

Brauzerda: http://127.0.0.1:8000/

## Imkoniyatlar

- **Telefon modeli** (majburiy) - iPhone 12, Samsung A52 va boshqalar
- **Klent telefon raqami** (majburiy)
- **Tuzalish narxi** - nechpulga tuzalishi (ixtiyoriy)
- **Zaklad summasi** - klent nechpul zaklad berib ketgani (ixtiyoriy)
- **Tayyor bo'lish sanasi** - qachonga tayyor qilish kerak (ixtiyoriy)
- **Kiritilgan vaqt** - avtomatik qo'yiladi
- **Qo'shimcha eslatmalar** (ixtiyoriy)

## Bazasi

SQLite - `db.sqlite3` fayli avtomatik yaratiladi.
