from django.utils import timezone
from .models import RepairOrder, ZapchastItem, ShopProfile


def user_shop_status(request):
    """Foydalanuvchi ustaxonaga ega ekanligini tekshiradi (template uchun)"""
    user_has_shop = False
    if request.user.is_authenticated:
        user_has_shop = ShopProfile.objects.filter(user=request.user).exists()
    return {'user_has_shop': user_has_shop}


def _shop_queryset(request, model):
    """Ustaxona bo'yicha filter (multi-tenant)"""
    if not request.user.is_authenticated or not hasattr(request.user, 'shop_profile'):
        return model.objects.none()
    return model.objects.filter(shop=request.user.shop_profile.shop)


def ready_phones_count(request):
    """Barcha template'larda tayyor telefonlar sonini ko'rsatish"""
    qs = _shop_queryset(request, RepairOrder)
    return {'ready_phones_count': qs.filter(status='ready').count()}


def zapchast_count(request):
    """Zapchast zakaz - olib kelinmagan zapchastlar soni"""
    qs = _shop_queryset(request, ZapchastItem)
    return {'zapchast_count': qs.filter(archived=False, is_done=False).count()}


def debt_reminder_count(request):
    """Qarzdorlar - muddati kelgan yoki o'tgan"""
    qs = _shop_queryset(request, RepairOrder)
    today = timezone.now().date()
    count = qs.filter(
        status='completed', has_debt=True,
        debt_deadline__lte=today
    ).exclude(debt_deadline__isnull=True).count()
    return {'debt_reminder_count': count}
