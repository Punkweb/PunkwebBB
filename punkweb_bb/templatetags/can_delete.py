from django import template

register = template.Library()


@register.filter
def can_delete(obj, user):
    return obj.can_delete(user)
