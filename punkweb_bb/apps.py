from django.apps import AppConfig


class PunkwebBbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "punkweb_bb"

    def ready(self):
        import punkweb_bb.signals
