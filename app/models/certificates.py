from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from .users import User
from . import Base


class Certificate(Base):
    __tablename__ = 'certificate'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    platform = Column(String(20))
    name = Column(String(50))
    type = Column(String(20))
    cert_pem = Column(Text)
    key_pem = Column(Text)
    token = Column(String(30))

    user = relationship(User, backref=backref('certificates', order_by=id, cascade='delete,all'))

    def __repr__(self):
        return "<Certificate('%d', '%s')>" % (self.id, self.name)
