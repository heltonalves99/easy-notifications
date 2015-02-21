from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from .certificates import Certificate
from . import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    log = Column(Text)
    created_at = Column(DateTime)

    certificate = relationship(Certificate, backref=backref('messages', order_by=id))

    def __repr__(self):
        return "<Message('%d', '%s')>" % (self.id, self.log[:10])
