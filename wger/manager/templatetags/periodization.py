from django import template
from wger.manager.helpers import periodization


register = template.Library()


@register.filter(name='perioditize')
def perioditize(duration):
    '''
    Takes duration value and returns appropriate periodization cycle.
    '''
    return periodization.translate(duration)
