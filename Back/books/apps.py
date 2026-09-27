from django.apps import AppConfig


class AllConfig(AppConfig):
    name = 'books'

    def ready(self):
        from . import signals
        return super().ready()