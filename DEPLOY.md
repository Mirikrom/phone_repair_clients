# Serverga qo'yish va ko'p ustaxonalar uchun yo'riqnoma

Bu loyiha **multi-tenant** tizimga ega: har bir ustaxona o'z ma'lumotlarini ko'radi, boshqa ustaxonalarning buyurtmalari va zapchastlari ko'rinmaydi.

---

## 1. Birinchi marta serverga qo'yish

### 1.1 Loyihani serverga yuklash

```bash
# Loyihani klonlash yoki yuklash
cd /var/www  # yoki boshqa papka
git clone <repo-url> phone_shop
cd phone_shop
```

### 1.2 Virtual muhit va kutubxonalar

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install gunicorn      # production uchun
```

### 1.3 Migratsiya va superuser

```bash
python manage.py migrate
python manage.py createsuperuser   # admin login/parol yarating
```

### 1.4 Birinchi ustaxona uchun foydalanuvchi

**Agar loyihada allaqachon ma'lumot bor bo'lsa** (migratsiyadan oldin buyurtmalar bo'lgan):

1. Django admin: `https://sizning-server.com/admin/`
2. Kirish: `createsuperuser` bilan yaratilgan login/parol
3. **Shop** (Ustaxona) — "Birinchi ustaxona" allaqachon yaratilgan bo'ladi
4. **Users** — yangi user yarating yoki mavjud userni tanlang
5. **Shop profiles** — yangi ShopProfile: User va Shop (Birinchi ustaxona) ni bog'lang

**Agar loyiha yangi bo'lsa** (ma'lumot yo'q):

1. Django admin: `https://sizning-server.com/admin/`
2. **Shop** (Ustaxona) — yangi Shop yarating
3. **Users** — yangi user yarating (**userlarni faqat admin yaratadi**)
4. **Shop profiles** — User va Shop ni bog'lang

---

## 2. Boshqa ustaga berish (yangi ustaxona)

Yangi usta uchun hisobni **admin** ochib beradi:

1. Admin panelda yangi **Shop** yarating (ustaxona)
2. Yangi **User** yarating (login/parol)
3. **ShopProfile** orqali User + Shop ni bog'lang
4. Ustaga login/parolni yuboring

---

## 3. Ko'p ustaxonalar — ma'lumotlar ajratilgan

Tizim **multi-tenant**:

| Narsa | Tavsif |
|-------|--------|
| **Har bir ustaxona** | O'z login va paroli bilan kiradi |
| **Ma'lumotlar** | Ustaxonalar bir-birining buyurtmalarini ko'rmaydi |
| **Yangi usta** | Hisobni admin yaratadi va ShopProfile bog'laydi |
| **Bitta server** | Barcha ustaxonalar bir serverda, lekin ma'lumotlar alohida |

---

## 4. Production server (misol: Ubuntu + Nginx)

### 4.1 Sozlamalar

`phone_shop/settings.py` da:

```python
DEBUG = False
ALLOWED_HOSTS = ['sizning-domain.com', 'www.sizning-domain.com', 'server-ip']
SECRET_KEY = 'juda-maxfiy-va-uzun-random-string'  # production uchun o'zgartiring!
```

### 4.2 Static fayllar

```bash
python manage.py collectstatic --noinput
```

### 4.3 Gunicorn

`gunicorn_config.py` yarating:

```python
bind = "127.0.0.1:8000"
workers = 3
chdir = "/var/www/phone_shop"
module = "phone_shop.wsgi:application"
```

Ishga tushirish:

```bash
gunicorn -c gunicorn_config.py
```

### 4.4 Nginx (ixtiyoriy)

```nginx
server {
    listen 80;
    server_name sizning-domain.com;
    location /static/ { alias /var/www/phone_shop/staticfiles/; }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 5. Tez-tez beriladigan savollar

**Q: Bir ustaxona uchun bir nechta foydalanuvchi bo'lishi mumkinmi?**  
A: Hozircha har bir hisob bitta ustaxonaga bog'langan. Kelajakda bir ustaxonaga bir nechta user qo'shish mumkin.

**Q: Ustalar bir-birining ma'lumotlarini ko'ra oladimi?**  
A: Yo'q. Har bir ustaxona faqat o'z buyurtmalari va zapchastlarini ko'radi.

**Q: Admin panel orqali barcha ma'lumotlarni ko'rish mumkinmi?**  
A: Ha. `createsuperuser` bilan yaratilgan admin barcha ustaxonalar va buyurtmalarni ko'radi (texnik boshqaruv uchun).

---

## 6. Xulosa

1. **Serverga qo'yish**: `migrate` → `createsuperuser` → (ixtiyoriy) birinchi ustaxona uchun ShopProfile
2. **Yangi usta**: admin yangi user + Shop + ShopProfile ochib beradi
3. **Ma'lumotlar**: Ustaxonalar o'rtasida ajratilgan, bir-biriga ko'rinmaydi
