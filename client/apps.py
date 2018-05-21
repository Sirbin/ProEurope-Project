from django.apps import AppConfig


class ClientConfig(AppConfig):
    name = 'client'
    verbose_name = 'Client Application'

    def ready(self):
        import client.signals
