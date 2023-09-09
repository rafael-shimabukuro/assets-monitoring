import os

from django.apps import AppConfig

from assets import settings


class AssetsMonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assets_monitoring'

    def ready(self):
        print("bomdia")
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.startAppScheduler()

