from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from certificates import Certificate
from . import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    certificate_id = Column(Integer, ForeignKey('certificates.id'))
    name = Column(String(50))
    token = Column(String(50))
    status = Column(Boolean)

    certificate = relationship(Certificate, backref=backref('devices', order_by=id))

    def __init__(self, certificate_id, name, token, status):
        self.certificate_id
        self.name = name
        self.token = token
        self.status = status

    def __repr__(self):
        return "<Device('%d', '%s')>" % (self.id, self.name)
