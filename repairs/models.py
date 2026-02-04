from django.db import models
from django.conf import settings


class Shop(models.Model):
    """Ustaxona - har bir ustaxona o'z ma'lumotlariga ega"""
    name = models.CharField(max_length=200, verbose_name='Ustaxona nomi')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ustaxona'
        verbose_name_plural = 'Ustaxonalar'

    def __str__(self):
        return self.name


class ShopProfile(models.Model):
    """Foydalanuvchi qaysi ustaxonaga tegishli"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shop_profile')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='users')

    class Meta:
        verbose_name = 'Ustaxona profil'
        verbose_name_plural = 'Ustaxona profillar'


class RepairOrder(models.Model):
    """Telefon ta'mirlash buyurtmasi - klentlar bilan ishlash uchun model"""
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders', null=True)
    phone_model = models.CharField(
        max_length=200,
        verbose_name='Telefon modeli'
    )
    client_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Mijoz ismi'
    )
    client_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Klent telefon raqami'
    )
    required_parts = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Qo\'yilish kerak bo\'lgan zapchast'
    )
    zapchast_olib_kelish_kerak = models.BooleanField(
        default=False,
        verbose_name='Zapchast olib kelish kerak'
    )
    repair_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Tuzalish narxi (so\'m)'
    )
    deposit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Zaklad summasi (so\'m)'
    )
    SCREEN_TYPE_CHOICES = [
        ('incell_abadoksiz', 'Incell abadoksiz'),
        ('incell_abadokli', 'Incell abadokli'),
        ('oled_abadokli', 'OLED abadokli'),
        ('oled_abadoksiz', 'OLED abadoksiz'),
        ('original_abadokli', 'Original abadokli'),
        ('original_abadoksiz', 'Original abadoksiz'),
        ('kbs', 'KBS'),
        ('kaiku', 'KAIKU'),
    ]
    
    screen_type = models.CharField(
        max_length=30,
        choices=SCREEN_TYPE_CHOICES,
        blank=True,
        verbose_name='Ekran turi'
    )
    
    LAMINAT_CHOICES = [
        ('laminat', 'Laminatsiya qo\'yib berish'),
        ('laminatsiz', 'Laminatsiya shart emas'),
    ]
    
    laminat = models.CharField(
        max_length=20,
        choices=LAMINAT_CHOICES,
        blank=True,
        verbose_name='Laminat'
    )
    
    READY_DEADLINE_CHOICES = [
        ('today_evening', 'Bugun kechga'),
        ('tomorrow_evening', 'Ertaga kechga'),
        ('2_3_days', '2-3 kundan keyin'),
    ]
    
    ready_deadline = models.CharField(
        max_length=20,
        choices=READY_DEADLINE_CHOICES,
        blank=True,
        verbose_name='Tayyor bo\'lish muddati'
    )
    ready_deadline_uncertain = models.BooleanField(
        default=False,
        verbose_name='Tayyor bo\'lish muddati hali aniq emas'
    )
    STATUS_CHOICES = [
        ('in_progress', 'Ta\'mirlanmoqda'),
        ('ready', 'Tayyor'),
        ('completed', 'Olib ketilgan'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress',
        verbose_name='Status'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Kiritilgan vaqt'
    )
    ready_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Tuzaldi sana'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Qo\'shimcha eslatmalar'
    )
    handover_notes = models.TextField(
        blank=True,
        verbose_name='Olib ketilganda eslatma (qarz bo\'lsa)'
    )
    has_debt = models.BooleanField(
        default=False,
        verbose_name='Qarzdor'
    )
    debt_deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name='Qarz to\'lanish muddati'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Olib ketilgan sana'
    )
    
    class Meta:
        verbose_name = 'Ta\'mirlash buyurtmasi'
        verbose_name_plural = 'Ta\'mirlash buyurtmalari'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.phone_model} - {self.client_phone}"

    @property
    def remaining_to_pay(self):
        """Mijozdan olinadigan pul: narx - zaklad"""
        if self.repair_cost is not None and self.deposit_amount is not None:
            return self.repair_cost - self.deposit_amount
        return None


class ZapchastItem(models.Model):
    """Zapchast zakaz ro'yxati - olib kelish kerak bo'lgan zapchastlar"""
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='zapchast_items', null=True)
    phone_model = models.CharField(max_length=200, blank=True, verbose_name='Telefon modeli')
    name = models.CharField(max_length=300, verbose_name='Zapchast nomi')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Soni')
    repair_order = models.ForeignKey(
        RepairOrder,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='zapchast_items',
        verbose_name='Buyurtma'
    )
    is_done = models.BooleanField(default=False, verbose_name='Olib kelingan')
    done_at = models.DateTimeField(null=True, blank=True, verbose_name='Olingan sana')
    archived = models.BooleanField(default=False, verbose_name='Istoriyaga yuborilgan')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Zapchast'
        verbose_name_plural = 'Zapchastlar'
    
    def __str__(self):
        return self.name
