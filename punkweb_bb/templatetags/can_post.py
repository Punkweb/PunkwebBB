from django import template

register = template.Library()


@register.filter
def can_post(obj, user):
    return obj.can_post(user)
