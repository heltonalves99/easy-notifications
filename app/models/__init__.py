import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

prod_engine = create_engine('sqlite:///database.sqlite3', echo=False)
dev_engine = create_engine('sqlite:///database.sqlite3', echo=False)
test_engine = create_engine('sqlite:///:memory:',
                            connect_args={'check_same_thread': False},
                            poolclass=StaticPool)

env = os.environ.get('APP_ENV', 'prod')

if env == 'prod':
    session = sessionmaker(bind=prod_engine)
elif env == 'dev':
    session = sessionmaker(bind=dev_engine)
else:
    session = sessionmaker(bind=test_engine)
