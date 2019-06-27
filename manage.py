from flask_script import Manager
from decouple import config as env_config
import coverage

cov = coverage.Coverage()
cov.start()

from api.app import app, scheduler

manager = Manager(app)

@manager.command
def run_server():
    app.run(
        env_config('HOST'),
        port=env_config('PORT'),
        debug=True
    )

@manager.command
def test():
    import pytest

    pytest.main([
        'tests',
        '--exitfirst',
        '-s',
    ])

    cov.stop()
    cov.save()
    cov.html_report()

@manager.command
def start_scheduler():
    scheduler.start()

if __name__ == "__main__":
    manager.run()
