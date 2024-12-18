from django.apps import AppConfig


class ConnectagroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'connectagro'

    def ready(self):
        import connectagro.signals  # Import the signals

