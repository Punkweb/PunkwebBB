from django import template
from django.template.defaultfilters import stringfilter

from punkweb_bb.parsers import get_shoutbox_parser

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def shoutbox_bbcode(value):
    parser = get_shoutbox_parser()

    return parser.render(value)
