import html
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from punkweb_bb.parsers import get_shoutbox_parser
from punkweb_bb.settings import RENDERER

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def shoutbox_render(value):
    if RENDERER == "bbcode":
        parser = get_shoutbox_parser()
        rendered = parser.render(value)
    elif RENDERER == "markdown":
        escaped = html.escape(value, quote=False)
        rendered = escaped

    return mark_safe(rendered)
