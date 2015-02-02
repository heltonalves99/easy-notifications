from sqlalchemy import Column, Integer, String
from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50))
    password = Column(String(100))

    def __repr__(self):
        return "<User('%d', '%s')>" % (self.id, self.username)
