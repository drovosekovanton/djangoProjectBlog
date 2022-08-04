from django.apps import AppConfig


class MiniblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miniblog'

    # def ready(self):
    #     # Implicitly connect signal handlers decorated with @receiver.
    #     from . import signals

