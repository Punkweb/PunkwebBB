from django.contrib.auth.models import Group
from django.utils.text import slugify


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


def get_user_highest_priority_group(user):
    groups = Group.objects.filter(user=user, style__isnull=False)

    if groups.exists():
        return groups.order_by("-style__priority").first()

    return None


def get_styled_username(user):
    group = get_user_highest_priority_group(user)

    if group:
        username_style = group.style.username_style
        styled_username = username_style.rendered.replace("{USER}", user.username)
        return styled_username
    else:
        return user.username


def get_group_name_styled(group):
    if group.style is None:
        return group.name
    else:
        username_style = group.style.username_style
        styled_group_name = username_style.rendered.replace("{USER}", group.name)
        return styled_group_name
