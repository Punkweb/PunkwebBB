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
