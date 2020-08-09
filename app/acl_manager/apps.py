from django.apps import AppConfig
from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler


class AclManagerConfig(AppConfig):
    name = 'app.acl_manager'

    def ready(self):
        from .service import dns_updater

        scheduler = BackgroundScheduler()
        scheduler.add_job(dns_updater.update_ips, 'interval', minutes=int(settings.SCHEDULE_UPDATE_TIME))
        scheduler.start()
