import bbcode


def add_font_tag(parser):
    def _render_font(name, value, options, parent, context):
        if "font" in options:
            font = options["font"].strip()
            return f'<span style="font-family:{font};">{value}</span>'
        return value

    parser.add_formatter("font", _render_font)


def add_size_tag(parser):
    def _render_size(name, value, options, parent, context):
        if "size" in options:
            size = options["size"].strip()
            return f'<font size="{size}">{value}</font>'
        return value

    parser.add_formatter("size", _render_size)


def add_color_tag(parser):
    def _render_color(name, value, options, parent, context):
        if "color" in options:
            color = options["color"].strip()
            return f'<span style="color: {color}">{value}</span>'
        return value

    parser.add_formatter("color", _render_color)


def add_shadow_tag(parser):
    def _render_shadow(name, value, options, parent, context):
        if "shadow" in options:
            shadow = options["shadow"].strip()
            return f'<span id="bbcode-shadow" style="text-shadow: 0px 0px 1em {shadow}">{value}</span>'
        return value

    parser.add_formatter("shadow", _render_shadow)


def add_url_tag(parser):
    def _render_url(name, value, options, parent, context):
        if "url" in options:
            url = options["url"]
            return f'<a href="{url}">{value}</a>'
        return f'<a href="{value}">{value}</a>'

    parser.add_formatter(
        "url", _render_url, replace_links=False, replace_cosmetic=False
    )


def add_quote_tag(parser):
    def _render_quote(name, value, options, parent, context):
        if "quote" in options:
            return f'<blockquote><cite>{options["quote"]} said: </cite>{value}</blockquote>'
        return f"<blockquote>{value}</blockquote>"

    parser.add_formatter(
        "quote", _render_quote, strip=True, swallow_trailing_newline=True
    )


def add_code_tag(parser):
    def _render_code(name, value, options, parent, context):
        if "code" in options:
            language = options["code"].strip()
            return f'<pre><code class="language-{language}">{value}</code></pre>'
        return f"<pre><code>{value}</code></pre>"

    parser.add_formatter(
        "code",
        _render_code,
        render_embedded=False,
        transform_newlines=False,
        replace_links=False,
        replace_cosmetic=False,
        strip=True,
        swallow_trailing_newline=True,
    )


def add_img_tag(parser):
    def _render_img(name, value, options, parent, context):
        if "width" in options:
            width = options["width"]
        if "height" in options:
            height = options["height"]

        if "width" in options and "height" in options:
            return (
                f'<img src="{value}" alt="{value}" width="{width}" height="{height}" />'
            )
        elif "width" in options:
            return f'<img src="{value}" alt="{value}" width="{width}" />'
        elif "height" in options:
            return f'<img src="{value}" alt="{value}" height="{height}" />'

        return f'<img src="{value}" alt="{value}" />'

    parser.add_formatter(
        "img",
        _render_img,
        render_embedded=False,
        replace_links=False,
        replace_cosmetic=False,
    )


def add_spoiler_tag(parser):
    def _render_spoiler(name, value, options, parent, context):
        if "spoiler" in options:
            summary = options["spoiler"]
            return f"<details><summary>{summary}</summary>{value}</details>"
        return f"<details><summary>Click to reveal</summary>{value}</details>"

    parser.add_formatter(
        "spoiler", _render_spoiler, strip=True, swallow_trailing_newline=True
    )


def init_text_tags(parser):
    parser.add_simple_formatter("b", "<strong>%(value)s</strong>")
    parser.add_simple_formatter("i", "<em>%(value)s</em>")
    parser.add_simple_formatter("u", "<u>%(value)s</u>")
    parser.add_simple_formatter("s", "<s>%(value)s</s>")
    parser.add_simple_formatter("sub", "<sub>%(value)s</sub>")
    parser.add_simple_formatter("sup", "<sup>%(value)s</sup>")
    parser.add_simple_formatter("escape", "%(value)s", render_embedded=False)

    add_color_tag(parser)
    add_shadow_tag(parser)
    add_font_tag(parser)
    add_url_tag(parser)


def init_alignment_tags(parser):
    parser.add_simple_formatter(
        "center", '<div style="text-align: center">%(value)s</div>'
    )
    parser.add_simple_formatter("left", '<div style="text-align: left">%(value)s</div>')
    parser.add_simple_formatter(
        "right", '<div style="text-align: right">%(value)s</div>'
    )


def init_list_tags(parser):
    parser.add_simple_formatter(
        "ol",
        "<ol>%(value)s</ol>",
        transform_newlines=False,
        strip=True,
        swallow_trailing_newline=True,
    )
    parser.add_simple_formatter(
        "ul",
        "<ul>%(value)s</ul>",
        transform_newlines=False,
        strip=True,
        swallow_trailing_newline=True,
    )
    parser.add_simple_formatter(
        "li",
        "<li>%(value)s</li>",
        newline_closes=True,
        transform_newlines=False,
        same_tag_closes=True,
        strip=True,
    )


def init_default_tags(parser):
    init_text_tags(parser)
    init_alignment_tags(parser)
    init_list_tags(parser)

    parser.add_simple_formatter("hr", "<hr />", standalone=True)
    add_size_tag(parser)
    add_img_tag(parser)
    add_quote_tag(parser)
    add_code_tag(parser)
    add_spoiler_tag(parser)


_parser = None
_mix_parser = None
_shoutbox_parser = None


def get_parser():
    global _parser
    if _parser is None:
        _parser = bbcode.Parser(
            install_defaults=False,
            replace_links=False,
            replace_cosmetic=False,
        )
        init_default_tags(_parser)
    return _parser


def get_shoutbox_parser():
    global _shoutbox_parser
    if _shoutbox_parser is None:
        _shoutbox_parser = bbcode.Parser(
            install_defaults=False, replace_links=False, replace_cosmetic=False
        )
        init_text_tags(_shoutbox_parser)
    return _shoutbox_parser


def get_mix_parser():
    global _mix_parser
    if _mix_parser is None:
        _mix_parser = bbcode.Parser(
            install_defaults=False,
            newline="\n",
            replace_links=False,
            replace_cosmetic=False,
            escape_html=False,
        )
        init_default_tags(_mix_parser)

    return _mix_parser
