from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from .certificates import Certificate
from . import Base


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    name = Column(String(50))
    token = Column(String(50))
    status = Column(Boolean)

    certificate = relationship(Certificate, backref=backref('devices', order_by=id))

    def __repr__(self):
        return "<Device('%d', '%s')>" % (self.id, self.name)
