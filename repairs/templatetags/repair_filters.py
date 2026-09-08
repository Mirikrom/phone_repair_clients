from django import template

register = template.Library()


@register.filter
def phone_without_prefix(value):
    """+998 ni olib tashlaydi: +998901234567 -> 90 123 45 67"""
    if not value:
        return ''
    s = str(value).strip()
    if s.startswith('+998'):
        return s[4:].lstrip()
    return s


@register.filter
def phone_tel_href(value):
    """Dialer uchun tel: havola. +998901234567 yoki 901234567 -> tel:+998901234567"""
    if not value:
        return ''
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    if not digits:
        return ''
    if digits.startswith('998') and len(digits) >= 12:
        return f'tel:+{digits}'
    if len(digits) == 9:
        return f'tel:+998{digits}'
    if digits.startswith('0') and len(digits) == 10:
        return f'tel:+998{digits[1:]}'
    return f'tel:+{digits}'


@register.filter
def intcomma_uz(value):
    """Raqamni vergul bilan ko'rsatadi: 200000 -> 200,000, 20000 -> 20,000"""
    if value is None:
        return ''
    try:
        num = int(float(value))
        return f'{num:,}'
    except (ValueError, TypeError):
        return str(value)


@register.filter
def money_dot_uz(value):
    """Raqamni nuqta bilan: 250000 -> 250.000 (etiketka uchun)"""
    if value is None:
        return ''
    try:
        num = int(float(value))
        return f'{num:,}'.replace(',', '.')
    except (ValueError, TypeError):
        return str(value)


@register.filter
def phone_digits(value):
    """Telefonni faqat raqam ko'rinishida (+998 siz): +998935319409 -> 935319409"""
    if not value:
        return ''
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    if digits.startswith('998') and len(digits) >= 12:
        return digits[3:]
    if digits.startswith('0') and len(digits) == 10:
        return digits[1:]
    return digits
