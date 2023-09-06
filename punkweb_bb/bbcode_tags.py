from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class CodeTag(BBCodeTag):
    name = "code"

    class Options:
        render_embedded = False
        strip = True
        transform_newlines = False

    def render(self, value, option=None, parent=None):
        if option is not None:
            return f"<pre><code class='language-{option}'>{value}</code></pre>"
        return f"<pre><code>{value}</code></pre>"


class EmailTag(BBCodeTag):
    name = "email"
    definition_string = "[email={TEXT1}]{TEXT2}[/email]"
    format_string = """<a href="mailto:{TEXT1}">{TEXT2}</a>"""


class FontTag(BBCodeTag):
    name = "font"
    definition_string = "[font={TEXT1}]{TEXT2}[/font]"
    format_string = '<span style="font-family:{TEXT1}">{TEXT2}</span>'


class HrTag(BBCodeTag):
    name = "hr"
    definition_string = "[hr]"
    format_string = "<hr/>"

    class Options:
        standalone = True


class LiTag(BBCodeTag):
    name = "li"
    definition_string = "[li]{TEXT}[/li]"
    format_string = "<li>{TEXT}</li>"


class OlTag(BBCodeTag):
    name = "ol"
    definition_string = "[ol]{TEXT}[/ol]"
    format_string = "<ol>{TEXT}</ol>"


class ShadowTag(BBCodeTag):
    name = "shadow"
    definition_string = "[shadow={TEXT1}]{TEXT2}[/shadow]"
    format_string = """<span id="bbcode-shadow" style="text-shadow: 0px 0px 1em {TEXT1}">{TEXT2}</span>"""


class SizeTag(BBCodeTag):
    name = "size"
    definition_string = "[size={RANGE=1,7}]{TEXT}[/size]"
    format_string = '<font size="{RANGE=1,7}">{TEXT}</font>'


class SubscriptTag(BBCodeTag):
    name = "sub"
    definition_string = "[sub]{TEXT}[/sub]"
    format_string = "<sub>{TEXT}</sub>"


class SuperscriptTag(BBCodeTag):
    name = "sup"
    definition_string = "[sup]{TEXT}[/sup]"
    format_string = "<sup>{TEXT}</sup>"


class UlTag(BBCodeTag):
    name = "ul"
    definition_string = "[ul]{TEXT}[/ul]"
    format_string = "<ul>{TEXT}</ul>"


tag_pool.register_tag(CodeTag)
tag_pool.register_tag(EmailTag)
tag_pool.register_tag(FontTag)
tag_pool.register_tag(HrTag)
tag_pool.register_tag(LiTag)
tag_pool.register_tag(OlTag)
tag_pool.register_tag(ShadowTag)
tag_pool.register_tag(SizeTag)
tag_pool.register_tag(SubscriptTag)
tag_pool.register_tag(SuperscriptTag)
tag_pool.register_tag(UlTag)
