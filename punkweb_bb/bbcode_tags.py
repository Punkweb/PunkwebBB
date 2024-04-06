from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class CheckedBoxBBCodeTag(BBCodeTag):
    name = "y"
    definition_string = "[y]{TEXT}"
    format_string = """<label style="display: block"><input type="checkbox" disabled="disabled" checked="checked" /> {TEXT}</label>"""

    class Options:
        newline_closes = True
        same_tag_closes = True
        end_tag_closes = True
        strip = True


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


class EscapeBBCodeTag(BBCodeTag):
    name = "escape"
    definition_string = "[escape]{TEXT}[/escape]"
    format_string = """<div class="escaped">{TEXT}</div>"""

    class Options:
        render_embedded = False


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


class LeftBBCodeTag(BBCodeTag):
    name = "left"
    definition_string = "[left]{TEXT}[/left]"
    format_string = """<div style="text-align: left">{TEXT}</div>"""


class LiBBCodeTag(BBCodeTag):
    name = "li"
    definition_string = "[li]{TEXT}[/li]"
    format_string = "<li>{TEXT}</li>"

    class Options:
        strip = True


class OlBBCodeTag(BBCodeTag):
    name = "ol"
    definition_string = "[ol]{TEXT}[/ol]"
    format_string = "<ol>{TEXT}</ol>"

    class Options:
        transform_newlines = False
        strip = True


class QuoteBBCodeTag(BBCodeTag):
    name = "quote"
    definition_string = "[quote={TEXT1}]{TEXT2}[/quote]"
    format_string = """
        <blockquote>
            <cite>
                {TEXT1} said:
            </cite>
            {TEXT2}
        </blockquote>"""


class RightBBCodeTag(BBCodeTag):
    name = "right"
    definition_string = "[right]{TEXT}[/right]"
    format_string = """<div style="text-align: right">{TEXT}</div>"""


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

    class Options:
        transform_newlines = False
        strip = True


class UncheckedBoxBBCodeTag(BBCodeTag):
    name = "n"
    definition_string = "[n]{TEXT}"
    format_string = """
        <label style="display: block"><input type="checkbox" disabled="disabled" /> {TEXT}</label>"""

    class Options:
        newline_closes = True
        same_tag_closes = True
        end_tag_closes = True
        strip = True


tag_pool.register_tag(CheckedBoxBBCodeTag)
tag_pool.register_tag(CodeBBCodeTag)
tag_pool.register_tag(EmailBBCodeTag)
tag_pool.register_tag(EscapeBBCodeTag)
tag_pool.register_tag(FontBBCodeTag)
tag_pool.register_tag(HrBBCodeTag)
tag_pool.register_tag(LeftBBCodeTag)
tag_pool.register_tag(LiBBCodeTag)
tag_pool.register_tag(OlBBCodeTag)
tag_pool.register_tag(QuoteBBCodeTag)
tag_pool.register_tag(RightBBCodeTag)
tag_pool.register_tag(ShadowBBCodeTag)
tag_pool.register_tag(SizeBBCodeTag)
tag_pool.register_tag(SubscriptBBCodeTag)
tag_pool.register_tag(SuperscriptBBCodeTag)
tag_pool.register_tag(UlBBCodeTag)
tag_pool.register_tag(UncheckedBoxBBCodeTag)
