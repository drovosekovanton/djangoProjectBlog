from django.apps import AppConfig


class MiniblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miniblog'

    # Signals are not used in this project
    # def ready(self):
    #     # Implicitly connect signal handlers decorated with @receiver.
    #     from . import signals

