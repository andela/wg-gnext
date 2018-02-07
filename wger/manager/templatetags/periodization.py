from django import template
from wger.manager.helpers import periodization


register = template.Library()


@register.filter(name='perioditize')
def perioditize(duration):
    return periodization.translate(duration)
