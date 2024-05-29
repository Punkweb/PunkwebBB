from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def styled_username(user):
    return mark_safe(user.profile.styled_username)
