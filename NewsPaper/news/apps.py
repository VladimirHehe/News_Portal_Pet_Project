from django.apps import AppConfig
from django.core.signals import setting_changed
from . import signals


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
