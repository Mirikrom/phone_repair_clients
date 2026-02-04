import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import RepairOrder, ZapchastItem, Shop, ShopProfile
from .forms import RepairOrderForm


def _parse_required_parts(required_parts_str):
    """Parse 'ekran x 2, batareya' -> [(name, qty), ...]"""
    result = []
    for part in [p.strip() for p in (required_parts_str or '').split(',') if p.strip()]:
        m = re.search(r'\s+x\s*(\d+)\s*$', part, re.IGNORECASE)
        if m:
            name = part[:m.start()].strip()
            qty = int(m.group(1))
        else:
            name = part
            qty = 1
        if name:
            result.append((name, max(1, qty)))
    return result


def _extract_part_names(required_parts_str):
    """Parse 'ekran x 2, batareya, LCD' -> ['ekran', 'batareya', 'LCD']"""
    names = []
    for part in [p.strip() for p in (required_parts_str or '').split(',') if p.strip()]:
        m = re.search(r'\s+x\s*(\d+)\s*$', part, re.IGNORECASE)
        name = part[:m.start()].strip() if m else part.strip()
        if name:
            names.append(name)
    return names


def login_view(request):
    """Kirish - bosh sahifa. Login/parol bo'lsa kirish, yo'q bo'lsa registerga."""
    if request.user.is_authenticated and ShopProfile.objects.filter(user=request.user).exists():
        next_url = request.GET.get('next') or request.POST.get('next', 'repairs:order_list')
        return redirect(next_url)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me') == 'on'
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                messages.error(request, 'Hisobingiz admin tomonidan tasdiqlanmagan. Kuting.')
                return render(request, 'repairs/login.html', {'no_profile': False})
            login(request, user)
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 kun eslab qolish
            else:
                request.session.set_expiry(0)  # Brauzer yopilganda chiqish
            if ShopProfile.objects.filter(user=user).exists():
                next_url = request.POST.get('next') or request.GET.get('next', 'repairs:order_list')
                return redirect(next_url)
            messages.warning(request, 'Sizda ustaxona profili yo\'q. Chiqib, yangi hisob bilan ro\'yxatdan o\'ting.')
            logout(request)
        else:
            messages.error(request, 'Login yoki parol noto\'g\'ri.')
    no_profile = request.user.is_authenticated and not ShopProfile.objects.filter(user=request.user).exists()
    return render(request, 'repairs/login.html', {'no_profile': no_profile})


def logout_view(request):
    """Chiqish"""
    logout(request)
    return redirect('repairs:login')


def register_view(request):
    """Yangi ustaxona ro'yxatdan o'tish. Parol ixtiyoriy (123 ham bo'ladi). Admin tasdiqlagach kirish mumkin."""
    if request.user.is_authenticated and ShopProfile.objects.filter(user=request.user).exists():
        return redirect('repairs:order_list')
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not shop_name or not username or not password:
            messages.error(request, 'Barcha maydonlarni to\'ldiring.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Bu login allaqachon band.')
        else:
            shop = Shop.objects.create(name=shop_name)
            user = User.objects.create_user(username=username, password=password, is_active=False)
            ShopProfile.objects.create(user=user, shop=shop)
            messages.success(request, f'Ro\'yxatdan o\'tdingiz! Admin tasdiqlagach kirishingiz mumkin.')
            return redirect('repairs:login')
    return render(request, 'repairs/register.html')


def autocomplete(request):
    """Avtomatik to'ldirish - telefon modeli va zapchast uchun oldingi qiymatlardan"""
    field = request.GET.get('field', '')
    q = (request.GET.get('q') or '').strip()
    if not field or len(q) < 1:
        return JsonResponse({'results': []})

    results = []
    q_lower = q.lower()

    shop = getattr(request, 'shop', None)
    if not shop:
        return JsonResponse({'results': []})

    if field == 'phone_model':
        models = RepairOrder.objects.filter(
            shop=shop, phone_model__icontains=q
        ).values_list('phone_model', flat=True).distinct()[:20]
        results = list(models)

    elif field == 'required_parts':
        seen = set()
        # ZapchastItem dan
        for name in ZapchastItem.objects.filter(shop=shop, name__icontains=q).values_list('name', flat=True).distinct()[:30]:
            if name and name.lower() not in seen:
                seen.add(name.lower())
                results.append(name)
        # RepairOrder.required_parts dan
        for rp in RepairOrder.objects.filter(shop=shop).exclude(required_parts='').values_list('required_parts', flat=True)[:500]:
            for name in _extract_part_names(rp):
                if q_lower in name.lower() and name.lower() not in seen:
                    seen.add(name.lower())
                    results.append(name)
        results = results[:20]

    return JsonResponse({'results': results})


def reminders_due(request):
    """Eslatmalar: vaqt keldi (shop bo'yicha)."""
    shop = getattr(request, 'shop', None)
    if not shop:
        return JsonResponse({'results': []})
    now = timezone.now()
    qs = RepairOrder.objects.filter(
        shop=shop,
        remind_at__isnull=False,
        remind_at__lte=now,
        reminder_fired_at__isnull=True,
    ).order_by('remind_at')[:20]
    results = []
    for o in qs:
        results.append({
            'id': o.pk,
            'phone_model': o.phone_model,
            'required_parts': o.required_parts or '',
            'client_name': o.client_name or '',
            'client_phone': o.client_phone or '',
            'remind_at': o.remind_at.isoformat() if o.remind_at else None,
        })
    return JsonResponse({'results': results})


def reminders_ack(request):
    """Eslatma berildi deb belgilash (qayta-qayta chiqmasin)."""
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)
    shop = getattr(request, 'shop', None)
    if not shop:
        return JsonResponse({'ok': False}, status=403)
    try:
        rid = int(request.POST.get('id', '0'))
    except (ValueError, TypeError):
        rid = 0
    if not rid:
        return JsonResponse({'ok': False}, status=400)
    now = timezone.now()
    updated = RepairOrder.objects.filter(shop=shop, pk=rid, reminder_fired_at__isnull=True).update(reminder_fired_at=now)
    return JsonResponse({'ok': bool(updated)})


def order_list(request):
    """Ta'mirlanayotgan buyurtmalar ro'yxati"""
    q = (request.GET.get('q') or '').strip()
    in_progress_orders = RepairOrder.objects.filter(shop=request.shop, status='in_progress')
    if q:
        digits = ''.join(ch for ch in q if ch.isdigit())
        cond = Q(phone_model__icontains=q)
        if digits:
            cond |= Q(client_phone__icontains=digits)
        in_progress_orders = in_progress_orders.filter(cond)
    in_progress_orders = in_progress_orders.order_by('-created_at')
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    return render(request, 'repairs/order_list.html', {
        'orders': in_progress_orders,
        'today': today,
        'yesterday': yesterday,
        'q': q,
    })


def ready_phones_list(request):
    """Tayyor bo'lgan telefonlar ro'yxati"""
    q = (request.GET.get('q') or '').strip()
    ready_orders = RepairOrder.objects.filter(shop=request.shop, status='ready')
    if q:
        digits = ''.join(ch for ch in q if ch.isdigit())
        cond = Q(phone_model__icontains=q)
        if digits:
            cond |= Q(client_phone__icontains=digits)
        ready_orders = ready_orders.filter(cond)
    ready_orders = ready_orders.order_by('-created_at')
    return render(request, 'repairs/ready_phones_list.html', {'ready_orders': ready_orders, 'q': q})


def debtors_list(request):
    """Qarzdorlar ro'yxati - olib ketilgan va qarzdor belgilangan buyurtmalar"""
    q = (request.GET.get('q') or '').strip()
    debtors = RepairOrder.objects.filter(shop=request.shop, status='completed', has_debt=True)
    if q:
        digits = ''.join(ch for ch in q if ch.isdigit())
        cond = Q(phone_model__icontains=q)
        if digits:
            cond |= Q(client_phone__icontains=digits)
        debtors = debtors.filter(cond)
    debtors = debtors.order_by('-created_at')
    today = timezone.now().date()
    return render(request, 'repairs/debtors_list.html', {'debtors': debtors, 'today': today, 'q': q})


def order_history(request):
    """Istoriya - olib ketilgan telefonlar yoki zapchastlar (tab bo'yicha).
    Default: Olib ketilgan telefonlar. Zapchastlar tab: faqat zapchastlar istoriyasi."""
    tab = request.GET.get('tab', 'phones')
    if tab not in ('phones', 'zapchast'):
        tab = 'phones'
    q = (request.GET.get('q') or '').strip()
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    if tab == 'zapchast':
        zapchast_items = ZapchastItem.objects.filter(shop=request.shop, archived=True)
        if q:
            zapchast_items = zapchast_items.filter(
                Q(phone_model__icontains=q) |
                Q(name__icontains=q) |
                Q(repair_order__phone_model__icontains=q)
            )
        zapchast_items = zapchast_items.order_by('-done_at', '-created_at')
        return render(request, 'repairs/order_history.html', {
            'orders': [],
            'zapchast_history': zapchast_items,
            'tab': tab,
            'today': today,
            'yesterday': yesterday,
            'q': q,
        })
    else:
        completed_orders = RepairOrder.objects.filter(shop=request.shop, status='completed')
        if q:
            digits = ''.join(ch for ch in q if ch.isdigit())
            cond = Q(phone_model__icontains=q)
            if digits:
                cond |= Q(client_phone__icontains=digits)
            completed_orders = completed_orders.filter(cond)
        completed_orders = completed_orders.order_by('-completed_at', '-created_at')
        return render(request, 'repairs/order_history.html', {
            'orders': completed_orders,
            'zapchast_history': [],
            'tab': tab,
            'today': today,
            'yesterday': yesterday,
            'q': q,
        })


def order_mark_ready(request, pk):
    """Ta'mirni tugatish - tayyor qilish (Tuzaldi bosilganda)"""
    order = get_object_or_404(RepairOrder, shop=request.shop, pk=pk)
    if order.status == 'in_progress':
        order.status = 'ready'
        order.ready_at = timezone.now()
        order.save()
        messages.success(request, 'Ta\'mir tugatildi! Telefon tayyor bo\'lganlar ro\'yxatiga qo\'shildi.')
    return redirect('repairs:order_list')


def order_mark_completed(request, pk):
    """Olib ketildi - mijoz telefonni oldi (modal yoki sahifa orqali)"""
    order = get_object_or_404(RepairOrder, shop=request.shop, pk=pk)
    if order.status != 'ready':
        return redirect('repairs:ready_phones_list')
    
    if request.method == 'POST':
        user_notes = request.POST.get('handover_notes', '').strip()
        has_debt = request.POST.get('has_debt') == 'on'
        debt_deadline = request.POST.get('debt_deadline', '').strip()
        if has_debt:
            order.handover_notes = 'To\'lovga qarz' + (' - ' + user_notes if user_notes else '')
        else:
            if order.repair_cost is not None:
                amt = int(order.repair_cost)
                order.handover_notes = f"To'lov {amt:,}"
            else:
                order.handover_notes = "To'lov"
        order.has_debt = has_debt
        if has_debt and debt_deadline:
            try:
                from datetime import datetime
                order.debt_deadline = datetime.strptime(debt_deadline, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                order.debt_deadline = None
        else:
            order.debt_deadline = None
        order.status = 'completed'
        order.completed_at = timezone.now()
        order.save()
        if has_debt:
            messages.success(request, 'Telefon olib ketildi! Qarzdorlar ro\'yxatiga qo\'shildi.')
        else:
            messages.success(request, 'Telefon olib ketildi! Arxivga qo\'shildi.')
        return redirect('repairs:ready_phones_list')
    
    return render(request, 'repairs/order_complete_confirm.html', {'order': order})


def order_create(request):
    """Yangi buyurtma qo'shish"""
    if request.method == 'POST':
        form = RepairOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.shop = request.shop
            order.save()
            if order.zapchast_olib_kelish_kerak and order.required_parts:
                for name, qty in _parse_required_parts(order.required_parts):
                    ZapchastItem.objects.create(shop=request.shop, name=name, quantity=qty, phone_model=order.phone_model, repair_order=order)
            messages.success(request, 'Buyurtma muvaffaqiyatli qo\'shildi!')
            return redirect('repairs:order_list')
        else:
            messages.error(request, 'Xatolik! Ma\'lumotlarni tekshiring.')
    else:
        form = RepairOrderForm()
    
    return render(request, 'repairs/order_form.html', {'form': form, 'title': 'Yangi buyurtma'})


def order_detail(request, pk):
    """Buyurtma tafsilotlari"""
    order = get_object_or_404(RepairOrder, shop=request.shop, pk=pk)
    today = timezone.now().date()
    return render(request, 'repairs/order_detail.html', {'order': order, 'today': today})


def order_print(request, pk):
    """Buyurtmani POS58 printer uchun pechat"""
    order = get_object_or_404(RepairOrder, shop=request.shop, pk=pk)
    return render(request, 'repairs/order_print.html', {'order': order})


def vizitka_choice(request):
    """Vizitka yoki carta nomerini chop etish tanlovi"""
    return render(request, 'repairs/vizitka_choice.html')


def vizitka_print(request):
    """Vizitka - Mirkomil +998903283313, POS-58 uchun"""
    return render(request, 'repairs/vizitka_print.html')


def carta_nomer_print(request):
    """Karta raqami - POS-58 uchun"""
    return render(request, 'repairs/carta_nomer_print.html')


def order_edit(request, pk):
    """Buyurtmani tahrirlash"""
    order = get_object_or_404(RepairOrder, shop=request.shop, pk=pk)
    if request.method == 'POST':
        form = RepairOrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            if order.zapchast_olib_kelish_kerak and order.required_parts:
                order.zapchast_items.all().delete()
                for name, qty in _parse_required_parts(order.required_parts):
                    ZapchastItem.objects.create(shop=request.shop, name=name, quantity=qty, phone_model=order.phone_model, repair_order=order)
            else:
                order.zapchast_items.all().delete()
            messages.success(request, 'Buyurtma yangilandi!')
            return redirect('repairs:order_list')
        else:
            messages.error(request, 'Xatolik! Ma\'lumotlarni tekshiring.')
    else:
        form = RepairOrderForm(instance=order)
    
    return render(request, 'repairs/order_form.html', {'form': form, 'order': order, 'title': 'Buyurtmani tahrirlash'})


def zapchast_zakaz_list(request):
    """Zapchast zakaz ro'yxati - olinmaganlar yuqorida, olindi (chiziqli) pastda.
    Tugatish bosilganda olindilar istoriyaga yuboriladi."""
    q = (request.GET.get('q') or '').strip()
    items = ZapchastItem.objects.filter(shop=request.shop, archived=False)
    if q:
        items = items.filter(
            Q(phone_model__icontains=q) |
            Q(name__icontains=q) |
            Q(repair_order__phone_model__icontains=q)
        )
    items = items.order_by('is_done', '-done_at', '-created_at')
    not_done_items = [i for i in items if not i.is_done]
    done_items = [i for i in items if i.is_done]
    return render(request, 'repairs/zapchast_zakaz_list.html', {
        'items': items,
        'not_done_items': not_done_items,
        'done_items': done_items,
        'has_done': bool(done_items),
        'q': q,
    })


def zapchast_mark_done(request):
    """Tanlangan zapchastlarni olindi qilish - ro'yxat pastiga chiziq bilan ko'chadi"""
    if request.method == 'POST':
        ids = request.POST.get('ids', '')
        if ids:
            try:
                pk_list = [int(x.strip()) for x in ids.split(',') if x.strip()]
                now = timezone.now()
                ZapchastItem.objects.filter(shop=request.shop, pk__in=pk_list, archived=False).update(is_done=True, done_at=now)
                messages.success(request, 'Tanlanganlar olindi belgilandi! Tugatish bosib istoriyaga yuboring.')
            except (ValueError, TypeError):
                pass
    return redirect('repairs:zapchast_zakaz_list')


def zapchast_tugatish(request):
    """Olindi belgilangan zapchastlarni istoriyaga yuborish.
    ids berilsa faqat shularni, aks holda barcha olindilarni yuboradi."""
    if request.method == 'POST':
        ids = request.POST.get('ids', '').strip()
        if ids:
            try:
                pk_list = [int(x.strip()) for x in ids.split(',') if x.strip()]
                count = ZapchastItem.objects.filter(shop=request.shop, pk__in=pk_list, archived=False, is_done=True).update(archived=True)
            except (ValueError, TypeError):
                count = 0
        else:
            count = ZapchastItem.objects.filter(shop=request.shop, archived=False, is_done=True).update(archived=True)
        if count:
            messages.success(request, f'{count} ta zapchast istoriyaga yuborildi!')
        else:
            messages.info(request, 'Istoriyaga yuboriladigan zapchast yo\'q.')
    return redirect('repairs:zapchast_zakaz_list')


def zapchast_toggle(request, pk):
    """Zapchast checkbox toggle - olindi/bekor (faqat ro'yxatdagi archived=False)"""
    item = get_object_or_404(ZapchastItem, shop=request.shop, pk=pk, archived=False)
    item.is_done = not item.is_done
    item.done_at = timezone.now() if item.is_done else None
    item.save()
    return redirect('repairs:zapchast_zakaz_list')


def zapchast_add(request):
    """Zapchast qo'shish - faqat telefon modeli bilan ham qo'shish mumkin"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone_model = request.POST.get('phone_model', '').strip()
        try:
            quantity = max(1, int(request.POST.get('quantity', 1)))
        except (ValueError, TypeError):
            quantity = 1
        if phone_model or name:
            display_name = name if name else (phone_model or '—')
            ZapchastItem.objects.create(shop=request.shop, name=display_name, phone_model=phone_model or '', quantity=quantity)
            messages.success(request, 'Zapchast qo\'shildi!')
        return redirect('repairs:zapchast_zakaz_list')
    return redirect('repairs:zapchast_zakaz_list')


def zapchast_edit(request, pk):
    """Zapchast tahrirlash"""
    item = get_object_or_404(ZapchastItem, shop=request.shop, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone_model = request.POST.get('phone_model', '').strip()
        try:
            quantity = max(1, int(request.POST.get('quantity', 1)))
        except (ValueError, TypeError):
            quantity = 1
        if phone_model or name:
            item.name = name if name else (phone_model or '—')
            item.phone_model = phone_model or ''
            item.quantity = quantity
            item.save()
            messages.success(request, 'Zapchast yangilandi!')
        return redirect('repairs:zapchast_zakaz_list')
    return render(request, 'repairs/zapchast_edit.html', {'item': item})


def zapchast_print(request):
    """Zapchast ro'yxatini POS58 printer uchun pechat - tanlanganlarni chiqaradi"""
    ids = request.GET.get('ids', '')
    if ids:
        try:
            pk_list = [int(x.strip()) for x in ids.split(',') if x.strip()]
            items = ZapchastItem.objects.filter(shop=request.shop, pk__in=pk_list, archived=False)
        except (ValueError, TypeError):
            items = ZapchastItem.objects.none()
    else:
        items = ZapchastItem.objects.none()
    return render(request, 'repairs/zapchast_print.html', {'items': items})


def zapchast_image(request):
    """Zapchast ro'yxatini katta jadvalda - screenshot yoki rasm saqlash uchun"""
    ids = request.GET.get('ids', '')
    if ids:
        try:
            pk_list = [int(x.strip()) for x in ids.split(',') if x.strip()]
            items = ZapchastItem.objects.filter(shop=request.shop, pk__in=pk_list, archived=False)
        except (ValueError, TypeError):
            items = ZapchastItem.objects.none()
    else:
        items = ZapchastItem.objects.none()
    return render(request, 'repairs/zapchast_image.html', {'items': items})


def zapchast_delete(request, pk):
    """Zapchast o'chirish"""
    item = get_object_or_404(ZapchastItem, shop=request.shop, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Zapchast o\'chirildi!')
        return redirect('repairs:zapchast_zakaz_list')
    return render(request, 'repairs/zapchast_confirm_delete.html', {'item': item})


def order_delete(request, pk):
    """Buyurtmani o'chirish"""
    order = get_object_or_404(RepairOrder, shop=request.shop, pk=pk)
    next_url = request.GET.get('next') or request.POST.get('next', 'repairs:order_list')
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Buyurtma o\'chirildi!')
        return redirect(next_url)
    return render(request, 'repairs/order_confirm_delete.html', {'order': order, 'next_url': next_url})
