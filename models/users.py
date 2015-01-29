from sqlalchemy import Column, Integer, String
from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User('%d', '%s')>" % (self.id, self.name)
