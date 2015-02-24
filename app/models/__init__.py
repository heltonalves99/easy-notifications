from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings import DB_ENGINE

Base = declarative_base()

session = sessionmaker(bind=DB_ENGINE)
db = session()
