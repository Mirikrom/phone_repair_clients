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
def intcomma_uz(value):
    """Raqamni vergul bilan ko'rsatadi: 200000 -> 200,000, 20000 -> 20,000"""
    if value is None:
        return ''
    try:
        num = int(float(value))
        return f'{num:,}'
    except (ValueError, TypeError):
        return str(value)
