from django.apps import AppConfig, apps


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Principal"

    def ready(self):

        try:
            axes_config = apps.get_app_config("axes")
            axes_config.verbose_name = "Segurança"
        except LookupError:
            pass
