from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base


class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    platform = Column(String(20))
    name = Column(String(50))
    type = Column(String(20))
    cert_pem = Column(Text)
    key_pem = Column(Text)

    user = relationship("User", backref=backref('certificates', order_by=id))

    def __init__(self, platform, name, type, cert_pem, key_pem):
        self.platform = platform
        self.name = name
        self.type = type
        self.cert_pem = cert_pem
        self.key_pem = key_pem

    def __repr__(self):
        return "<Certificate('%d', '%s')>" % (self.id, self.name)
