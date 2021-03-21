from urllib.parse import urlencode
from django import template
from iso_language_codes import language_name

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    query.update(kwargs)
    return query.urlencode()


@register.simple_tag()
def decode_language(code):
    code = language_name(code)
    return code