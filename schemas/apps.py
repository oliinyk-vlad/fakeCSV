from django.apps import AppConfig


class SchemasConfig(AppConfig):
    name = 'schemas'

    def ready(self):
        import schemas.signals
