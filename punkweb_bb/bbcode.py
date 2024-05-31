import bbcode


def render_color(name, value, options, parent, context):
    if "color" in options:
        color = options["color"].strip()
        return f'<span style="color: {color}">{value}</span>'
    return value


def render_shadow(name, value, options, parent, context):
    if "shadow" in options:
        shadow = options["shadow"].strip()
        return f'<span id="bbcode-shadow" style="text-shadow: 0px 0px 1em {shadow}">{value}</span>'
    return value


def render_font(name, value, options, parent, context):
    if "font" in options:
        font = options["font"].strip()
        return f'<span style="font-family:{font};">{value}</span>'
    return value


def render_quote(name, value, options, parent, context):
    if "quote" in options:
        return f'<blockquote><cite>{options["quote"]} said: </cite>{value}</blockquote>'
    return f"<blockquote>{value}</blockquote>"


def render_code(name, value, options, parent, context):
    if "code" in options:
        language = options["code"].strip()
        return f'<pre><code class="language-{language}">{value}</code></pre>'
    return f"<pre><code>{value}</code></pre>"


def render_img(name, value, options, parent, context):
    if "width" in options:
        width = options["width"]
    if "height" in options:
        height = options["height"]

    if "width" in options and "height" in options:
        return f'<img src="{value}" alt="{value}" width="{width}" height="{height}" />'
    elif "width" in options:
        return f'<img src="{value}" alt="{value}" width="{width}" />'
    elif "height" in options:
        return f'<img src="{value}" alt="{value}" height="{height}" />'

    return f'<img src="{value}" alt="{value}" />'


def render_url(name, value, options, parent, context):
    if "url" in options:
        url = options["url"]
        return f'<a href="{url}">{value}</a>'
    return f'<a href="{value}">{value}</a>'


def render_size(name, value, options, parent, context):
    if "size" in options:
        size = options["size"].strip()
        return f'<font size="{size}">{value}</font>'
    return value


def init_default_tags(parser):
    parser.add_simple_formatter("b", "<strong>%(value)s</strong>")
    parser.add_simple_formatter("i", "<em>%(value)s</em>")
    parser.add_simple_formatter("u", "<u>%(value)s</u>")
    parser.add_simple_formatter("s", "<s>%(value)s</s>")
    parser.add_simple_formatter("sub", "<sub>%(value)s</sub>")
    parser.add_simple_formatter("sup", "<sup>%(value)s</sup>")
    parser.add_simple_formatter("escape", "%(value)s", render_embedded=False)

    parser.add_formatter("font", render_font)
    parser.add_formatter("color", render_color)
    parser.add_formatter("shadow", render_shadow)
    parser.add_formatter("url", render_url, replace_links=False, replace_cosmetic=False)


_parser = None
_shoutbox_parser = None


def get_parser():
    global _parser
    if _parser is None:
        _parser = bbcode.Parser(install_defaults=False)
        init_default_tags(_parser)

        _parser.add_simple_formatter("hr", "<hr />", standalone=True)
        _parser.add_simple_formatter(
            "center", '<div style="text-align: center">%(value)s</div>'
        )
        _parser.add_simple_formatter(
            "left", '<div style="text-align: left">%(value)s</div>'
        )
        _parser.add_simple_formatter(
            "right", '<div style="text-align: right">%(value)s</div>'
        )
        _parser.add_simple_formatter(
            "ol",
            "<ol>%(value)s</ol>",
            transform_newlines=False,
            strip=True,
            swallow_trailing_newline=True,
        )
        _parser.add_simple_formatter(
            "ul",
            "<ul>%(value)s</ul>",
            transform_newlines=False,
            strip=True,
            swallow_trailing_newline=True,
        )
        _parser.add_simple_formatter(
            "li",
            "<li>%(value)s</li>",
            newline_closes=True,
            transform_newlines=False,
            same_tag_closes=True,
            strip=True,
        )

        _parser.add_formatter("size", render_size)
        _parser.add_formatter(
            "img",
            render_img,
            render_embedded=False,
            replace_links=False,
            replace_cosmetic=False,
        )
        _parser.add_formatter(
            "quote", render_quote, strip=True, swallow_trailing_newline=True
        )
        _parser.add_formatter(
            "code",
            render_code,
            render_embedded=False,
            transform_newlines=False,
            replace_links=False,
            replace_cosmetic=False,
            strip=True,
            swallow_trailing_newline=True,
        )
    return _parser


def get_shoutbox_parser():
    global _shoutbox_parser
    if _shoutbox_parser is None:
        _shoutbox_parser = bbcode.Parser(install_defaults=False)
        init_default_tags(_shoutbox_parser)
    return _shoutbox_parser
