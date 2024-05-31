from django.forms import Textarea
from django.utils.text import slugify

from punkweb_bb.bbcode import get_parser
from punkweb_bb.settings import PARSER
from punkweb_bb.widgets import BBCodeEditorWidget, MarkdownEditorWidget


def get_editor_widget():
    if PARSER == "bbcode":
        return BBCodeEditorWidget()
    elif PARSER == "markdown":
        return MarkdownEditorWidget()
    return Textarea(attrs={"class": "pw-input"})


def get_unique_slug(model, field):
    base_slug = slugify(field)
    slug = base_slug
    unique_slug_exists = True

    counter = 1
    while unique_slug_exists:
        if model.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        else:
            unique_slug_exists = False

    return slug


def get_highest_priority_group(user):
    groups = user.groups.filter(style__isnull=False)

    if groups.exists():
        return groups.order_by("-style__priority").first()

    return None


def get_styled_username(user):
    group = get_highest_priority_group(user)

    if group:
        parser = get_parser()
        username_style = group.style.username_style
        rendered = parser.format(username_style.replace("{USER}", user.username))
        return rendered

    return user.username


def get_styled_group_name(group):
    if group.style is not None:
        parser = get_parser()
        username_style = group.style.username_style
        rendered = parser.format(username_style.replace("{USER}", group.name))
        return rendered

    return group.name
