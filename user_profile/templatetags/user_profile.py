from django import template


register = template.Library()


@register.simple_tag
def user_has_perm(user, perm):
    print(user, perm)
    return user.has_perm(perm)
