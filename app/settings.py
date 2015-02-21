import os
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

APP_ENV = os.environ.get('APP_ENV', 'dev')
DEBUG = True if APP_ENV in ['dev', 'test'] else False

ENGINES = {
    'dev': create_engine('sqlite:///database.sqlite3', echo=False),
    'prod': create_engine('sqlite:///database.sqlite3', echo=False),
    'test': create_engine('sqlite:///:memory:',
                          connect_args={'check_same_thread': False},
                          poolclass=StaticPool)
}

DB_ENGINE = ENGINES[APP_ENV]
