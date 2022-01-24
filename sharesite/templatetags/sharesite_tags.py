from django import template
import pytz

register = template.Library()

@register.tag
def set_timezones(parser, token):
    return TimezoneNode()


class TimezoneNode(template.Node):
    def render(self, context):
        context['common_timezones'] = pytz.common_timezones
        return ''