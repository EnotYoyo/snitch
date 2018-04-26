import os

TESTING = True
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'this is debug'

if 'SNITCH_DB_URI' not in os.environ:
    from snitch.config.postgres_config import config as postgres
    os.environ['SNITCH_DB_URI'] = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(**postgres)

SQLALCHEMY_DATABASE_URI = os.environ['SNITCH_DB_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False
