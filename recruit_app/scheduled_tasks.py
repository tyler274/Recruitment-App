from redis import Redis

from rq_scheduler import Scheduler

from recruit_app.user.tasks import run_alliance_corp_update, run_character_update

import datetime as dt

scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue


def schedule_tasks():
    scheduler.schedule(
         scheduled_time=dt.datetime.now(),  # Time for first execution, in UTC timezone
         func=run_alliance_corp_update,                     # Function to be queued
         interval=21600,                   # Time before the function is called again, in seconds
         queue_name='low',
    )
    # scheduler_low.schedule(
    #     scheduled_time=dt.datetime.now(),  # Time for first execution, in UTC timezone
    #     func=run_character_update,                     # Function to be queued
    #     interval=10800,                   # Time before the function is called again, in seconds
    # )
    # run_alliance_corp_update.delay()
    pass