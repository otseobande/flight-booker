from decouple import config as env_config

class Config(object):
    ENV = env_config('ENV', default='production')
    DEBUG = env_config('DEBUG', default=False, cast=bool)
    SECRET_KEY = env_config('SECRET_KEY')
    MONGODB_SETTINGS = {
        'host': env_config('MONGO_URL')
    }

