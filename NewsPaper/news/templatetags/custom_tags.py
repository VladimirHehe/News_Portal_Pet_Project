from datetime import datetime
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template import Library
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()

