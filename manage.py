from flask_script import Manager
from decouple import config as env_config

from api.app import app

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
        '--cov-config=.coveragerc',
        '--cov=api'
    ])

if __name__ == "__main__":
    manager.run()
