import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from django_apscheduler.jobstores import DjangoJobStore

from assets_monitoring.tasks import update_asset_prices


def my_task():
    print("looking for assets to be updated", datetime.datetime.now())
    update_asset_prices()


scheduler = BackgroundScheduler()


def startAppScheduler():
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.remove_all_jobs()
    trigger = IntervalTrigger(seconds=60)
    scheduler.add_job(my_task, trigger=trigger, replace_existing=True, id="assetsMonitoring")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
