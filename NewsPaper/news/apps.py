from django.apps import AppConfig
from importlib import import_module
from django.apps import apps


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        for app_config in apps.get_app_configs():
            base = app_config.module.__name__
            try:
                import_module(f"{base}.signals")
            except ImportError:
                pass
