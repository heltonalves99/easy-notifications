from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///database.sqlite3', echo=False)
test_engine = create_engine('sqlite:///:memory:',
                            connect_args={'check_same_thread': False},
                            poolclass=StaticPool)
