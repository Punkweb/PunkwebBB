from django import template
from django.utils.safestring import mark_safe

from punkweb_bb.utils import get_group_name_styled

register = template.Library()


@register.filter
def styled_group_name(group):
    return mark_safe(get_group_name_styled(group))
