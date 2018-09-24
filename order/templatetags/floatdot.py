from django.template import Library

register = Library()

@register.filter(name='floatdot')
def floatdot(value):
    return "{0:.2f}".format(value)

floatdot.is_safe = True


register.filter(floatdot)