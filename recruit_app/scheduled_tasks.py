from flask import current_app
from redis import Redis

from rq_scheduler import Scheduler

from recruit_app.user.tasks import run_alliance_corp_update, run_api_key_update

import datetime as dt

scheduler = Scheduler(connection=Redis())  # Get a scheduler for the "default" queue


def schedule_tasks():
    scheduler.schedule(
        scheduled_time=dt.datetime.now(),
        func=run_alliance_corp_update,
        interval=21600,
        queue_name='low',
        )
    scheduler.schedule(
        scheduled_time=dt.datetime.now(),
        func=run_api_key_update,
        interval=10800,
        queue_name='low',
        )
    return None