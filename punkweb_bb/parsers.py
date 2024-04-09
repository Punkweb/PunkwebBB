from django.apps import apps
from precise_bbcode.bbcode.parser import BBCodeParser
from precise_bbcode.bbcode.placeholder import BBCodePlaceholder
from precise_bbcode.core.loading import get_subclasses

_shoutbox_parser = None


def get_shoutbox_parser():
    if not _shoutbox_parser:
        loader = ShoutboxParserLoader()
        loader.load_parser()
    return _shoutbox_parser


class ShoutboxParserLoader(object):
    def __init__(self, *args, **kwargs):
        global _shoutbox_parser
        _shoutbox_parser = BBCodeParser()
        self.parser = _shoutbox_parser

    def load_parser(self):
        self.init_default_bbcode_placeholders()
        self.init_bbcode_placeholders()
        self.init_default_bbcode_tags()
        self.init_bbcode_tags()
        self.init_bbcode_smilies()

    def init_default_bbcode_placeholders(self):
        import precise_bbcode.bbcode.defaults.placeholder

        for placeholder_klass in get_subclasses(
            precise_bbcode.bbcode.defaults.placeholder, BBCodePlaceholder
        ):
            setattr(placeholder_klass, "default_placeholder", True)
            self.parser.add_placeholder(placeholder_klass)

    def init_bbcode_placeholders(self):
        from precise_bbcode.placeholder_pool import placeholder_pool

        placeholders = placeholder_pool.get_placeholders()
        for placeholder in placeholders:
            self.parser.add_placeholder(placeholder)

    def init_default_bbcode_tags(self):
        import precise_bbcode.bbcode.defaults.tag

        self.parser.add_bbcode_tag(precise_bbcode.bbcode.defaults.tag.StrongBBCodeTag)
        self.parser.add_bbcode_tag(precise_bbcode.bbcode.defaults.tag.ItalicBBCodeTag)
        self.parser.add_bbcode_tag(
            precise_bbcode.bbcode.defaults.tag.UnderlineBBCodeTag
        )
        self.parser.add_bbcode_tag(precise_bbcode.bbcode.defaults.tag.StrikeBBCodeTag)
        self.parser.add_bbcode_tag(precise_bbcode.bbcode.defaults.tag.ColorBBCodeTag)
        self.parser.add_bbcode_tag(precise_bbcode.bbcode.defaults.tag.UrlBBCodeTag)

    def init_bbcode_tags(self):
        import punkweb_bb.bbcode_tags

        self.parser.add_bbcode_tag(punkweb_bb.bbcode_tags.FontBBCodeTag)
        self.parser.add_bbcode_tag(punkweb_bb.bbcode_tags.ShadowBBCodeTag)
        self.parser.add_bbcode_tag(punkweb_bb.bbcode_tags.SubscriptBBCodeTag)
        self.parser.add_bbcode_tag(punkweb_bb.bbcode_tags.SuperscriptBBCodeTag)

    def init_bbcode_smilies(self):
        SmileyTag = apps.get_model("precise_bbcode", "SmileyTag")
        if SmileyTag:
            custom_smilies = SmileyTag.objects.all()
            for smiley in custom_smilies:
                self.parser.add_smiley(smiley.code, smiley.html_code)
