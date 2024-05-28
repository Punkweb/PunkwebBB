from django import template

register = template.Library()


@register.filter
def can_edit(obj, user):
    return obj.can_edit(user)
