from datetime import datetime
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template import Library
from django import template
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.filter
def translate_category(category):
    language_code = get_language()
    return category.title if language_code == 'en' else getattr(category, f'title_{language_code}')
