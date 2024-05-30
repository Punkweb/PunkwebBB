import html
from io import StringIO

import markdown as md
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from precise_bbcode.bbcode import get_parser

from punkweb_bb.settings import RENDERER

register = template.Library()


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


md.Markdown.output_formats["plain"] = unmark_element
unmark = md.Markdown(output_format="plain")
unmark.stripTopLevelTags = False


@register.filter(is_safe=True)
@stringfilter
def render(value):
    if RENDERER == "bbcode":
        parser = get_parser()
        rendered = parser.render(value)
    elif RENDERER == "markdown":
        escaped = html.escape(value, quote=False)
        rendered = md.markdown(escaped, extensions=["markdown.extensions.fenced_code"])

    return mark_safe(rendered)


@register.filter()
@stringfilter
def unmarkdown(value):
    return unmark.convert(value)
