from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class CodeBBCodeTag(BBCodeTag):
    name = "code"

    class Options:
        render_embedded = False
        strip = True
        transform_newlines = False

    def render(self, value, option=None, parent=None):
        if option is not None:
            return f"<pre><code class='language-{option}'>{value}</code></pre>"
        return f"<pre><code>{value}</code></pre>"


class EmailBBCodeTag(BBCodeTag):
    name = "email"
    definition_string = "[email={TEXT1}]{TEXT2}[/email]"
    format_string = """<a href="mailto:{TEXT1}">{TEXT2}</a>"""


class FontBBCodeTag(BBCodeTag):
    name = "font"
    definition_string = "[font={TEXT1}]{TEXT2}[/font]"
    format_string = '<span style="font-family:{TEXT1}">{TEXT2}</span>'


class HrBBCodeTag(BBCodeTag):
    name = "hr"
    definition_string = "[hr]"
    format_string = "<hr/>"

    class Options:
        standalone = True


class LiBBCodeTag(BBCodeTag):
    name = "li"
    definition_string = "[li]{TEXT}[/li]"
    format_string = "<li>{TEXT}</li>"


class OlBBCodeTag(BBCodeTag):
    name = "ol"
    definition_string = "[ol]{TEXT}[/ol]"
    format_string = "<ol>{TEXT}</ol>"


class ShadowBBCodeTag(BBCodeTag):
    name = "shadow"
    definition_string = "[shadow={TEXT1}]{TEXT2}[/shadow]"
    format_string = """<span id="bbcode-shadow" style="text-shadow: 0px 0px 1em {TEXT1}">{TEXT2}</span>"""


class SizeBBCodeTag(BBCodeTag):
    name = "size"
    definition_string = "[size={RANGE=1,7}]{TEXT}[/size]"
    format_string = '<font size="{RANGE=1,7}">{TEXT}</font>'


class SubscriptBBCodeTag(BBCodeTag):
    name = "sub"
    definition_string = "[sub]{TEXT}[/sub]"
    format_string = "<sub>{TEXT}</sub>"


class SuperscriptBBCodeTag(BBCodeTag):
    name = "sup"
    definition_string = "[sup]{TEXT}[/sup]"
    format_string = "<sup>{TEXT}</sup>"


class UlBBCodeTag(BBCodeTag):
    name = "ul"
    definition_string = "[ul]{TEXT}[/ul]"
    format_string = "<ul>{TEXT}</ul>"


tag_pool.register_tag(CodeBBCodeTag)
tag_pool.register_tag(EmailBBCodeTag)
tag_pool.register_tag(FontBBCodeTag)
tag_pool.register_tag(HrBBCodeTag)
tag_pool.register_tag(LiBBCodeTag)
tag_pool.register_tag(OlBBCodeTag)
tag_pool.register_tag(ShadowBBCodeTag)
tag_pool.register_tag(SizeBBCodeTag)
tag_pool.register_tag(SubscriptBBCodeTag)
tag_pool.register_tag(SuperscriptBBCodeTag)
tag_pool.register_tag(UlBBCodeTag)
