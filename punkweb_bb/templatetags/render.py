import html

import markdown as md
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from punkweb_bb.bbcode import get_parser, get_shoutbox_parser
from punkweb_bb.settings import PARSER

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def render(value):
    if PARSER == "bbcode":
        parser = get_parser()
        rendered = parser.format(value)
        return mark_safe(rendered)
    elif PARSER == "markdown":
        escaped = html.escape(value)
        rendered = md.markdown(escaped, extensions=["markdown.extensions.fenced_code"])
        return mark_safe(rendered)
    return value


@register.filter(is_safe=True)
@stringfilter
def render_shout(value):
    if PARSER == "bbcode":
        parser = get_shoutbox_parser()
        rendered = parser.format(value)
        return mark_safe(rendered)
    return value
