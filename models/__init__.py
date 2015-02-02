from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///database.sqlite3', echo=False)
test_engine = create_engine('sqlite:///test_database.sqlite3', echo=False)
