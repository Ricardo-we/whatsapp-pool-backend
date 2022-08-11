from dataclasses import replace
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from cron_validator import CronValidator

scheduler = BackgroundScheduler()


def start_schedule(func, id, minutes=0, seconds=0,  type="interval", max_instances=1, **kwargs):
    scheduler = BackgroundScheduler()
    schedule = scheduler.add_job(
        func,
        type,
        id=id,
        minutes=minutes,
        max_instances=max_instances,
        seconds=seconds,
        replace_existing=True,
        kwargs=kwargs
    )
    scheduler.start()
    return schedule


def cron_scheduler(func, id, cron_expression):
    scheduler = BackgroundScheduler()
    schedule = scheduler.add_job(
        func,
        CronTrigger.from_crontab(cron_expression),
        id=id,
        replace_existing=True,
        max_instances=1
    )
    scheduler.start()
    return schedule


def delete_job_if_exists(job_id):
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        return True
    return False


def validate_cron_exp(cron_expression):
    assert CronValidator.parse(cron_expression) is not None
