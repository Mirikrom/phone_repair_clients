from django.contrib import admin
from .models import RepairOrder, Shop, ShopProfile, ZapchastItem


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'shop']
    list_filter = ['shop']


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ['phone_model', 'client_phone', 'shop', 'status', 'repair_cost', 'deposit_amount', 'screen_type', 'laminat', 'ready_deadline', 'created_at']
    list_filter = ['shop', 'status', 'created_at', 'ready_deadline']
    search_fields = ['phone_model', 'client_phone']


@admin.register(ZapchastItem)
class ZapchastItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_model', 'shop', 'quantity', 'is_done', 'archived', 'created_at']
    list_filter = ['shop', 'is_done', 'archived']
