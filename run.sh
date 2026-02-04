#!/bin/bash
# Telefon Ustaxonasi - Serverni ishga tushirish

cd "$(dirname "$0")"

# Virtual muhit yaratish (agar yo'q bo'lsa)
if [ ! -d "venv" ]; then
    echo "Virtual muhit yaratilmoqda..."
    python3 -m venv venv
fi

# Virtual muhitdagi Python ishlatiladi (activate shart emas)
PYTHON=venv/bin/python

# Django o'rnatish
$PYTHON -m pip install Django -q 2>/dev/null || $PYTHON -m pip install Django --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Migratsiyalar
$PYTHON manage.py migrate -q 2>/dev/null

# Server ishga tushirish
echo "Server ishga tushmoqda: http://127.0.0.1:8000/"
$PYTHON manage.py runserver
