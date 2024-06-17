from django import template
from punkweb_bb import settings

register = template.Library()


@register.simple_tag
def punkweb_bb(setting_name, default=None):
    return getattr(settings, setting_name, default)
