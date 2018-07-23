from django import template

register = template.Library()


@register.simple_tag
def get_price_for_user(user, package):
    return package.make_price_for_user(user)
