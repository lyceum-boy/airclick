from django import template

register = template.Library()


@register.filter
def format_price(value):
    try:
        return f"{value:,} ₽".replace(",", " ")
    except (ValueError, TypeError):
        return value


@register.filter
def format_duration(value):
    try:
        hours = value // 60
        minutes = value % 60
        return f"{hours} ч. {minutes} мин." if hours else f"{minutes} мин."
    except (ValueError, TypeError):
        return value


@register.filter
def multiply(value, arg):
    return value * arg
