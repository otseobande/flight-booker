from apscheduler.schedulers.background import BlockingScheduler

# jobs
from api.jobs.reminders import remind_users_of_upcoming_flights

scheduler = BlockingScheduler()

scheduler.add_job(
    remind_users_of_upcoming_flights,
    'cron',
    hour=18
)
