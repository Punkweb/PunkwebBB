from django.apps import apps
from precise_bbcode.bbcode.defaults.tag import (
    ColorBBCodeTag,
    ItalicBBCodeTag,
    StrikeBBCodeTag,
    StrongBBCodeTag,
    UnderlineBBCodeTag,
    UrlBBCodeTag,
)
from precise_bbcode.bbcode.parser import BBCodeParser
from precise_bbcode.bbcode.placeholder import BBCodePlaceholder
from precise_bbcode.core.loading import get_subclasses

from punkweb_bb.bbcode_tags import (
    FontBBCodeTag,
    ShadowBBCodeTag,
    SubscriptBBCodeTag,
    SuperscriptBBCodeTag,
)

shoutbox_parser = BBCodeParser()


def init_default_bbcode_placeholders():
    import precise_bbcode.bbcode.defaults.placeholder

    for placeholder_klass in get_subclasses(
        precise_bbcode.bbcode.defaults.placeholder, BBCodePlaceholder
    ):
        setattr(placeholder_klass, "default_placeholder", True)
        shoutbox_parser.add_placeholder(placeholder_klass)


def init_bbcode_placeholders():
    from precise_bbcode.placeholder_pool import placeholder_pool

    placeholders = placeholder_pool.get_placeholders()
    for placeholder in placeholders:
        shoutbox_parser.add_placeholder(placeholder)


def init_bbcode_tags():
    shoutbox_parser.add_bbcode_tag(StrongBBCodeTag)
    shoutbox_parser.add_bbcode_tag(ItalicBBCodeTag)
    shoutbox_parser.add_bbcode_tag(UnderlineBBCodeTag)
    shoutbox_parser.add_bbcode_tag(StrikeBBCodeTag)
    shoutbox_parser.add_bbcode_tag(ColorBBCodeTag)
    shoutbox_parser.add_bbcode_tag(UrlBBCodeTag)
    shoutbox_parser.add_bbcode_tag(FontBBCodeTag)
    shoutbox_parser.add_bbcode_tag(ShadowBBCodeTag)
    shoutbox_parser.add_bbcode_tag(SubscriptBBCodeTag)
    shoutbox_parser.add_bbcode_tag(SuperscriptBBCodeTag)


def init_bbcode_smilies():
    SmileyTag = apps.get_model("precise_bbcode", "SmileyTag")
    if SmileyTag:
        custom_smilies = SmileyTag.objects.all()
        for smiley in custom_smilies:
            shoutbox_parser.add_smiley(smiley.code, smiley.html_code)


init_default_bbcode_placeholders()
init_bbcode_placeholders()
init_bbcode_tags()
init_bbcode_smilies()
