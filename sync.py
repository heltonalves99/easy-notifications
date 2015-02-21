from app.models.users import User  # noqa
from app.models.devices import Device  # noqa
from app.models.certificates import Certificate  # noqa
from app.models.console import Message  # noqa
from app import models
from app.settings import DB_ENGINE

try:
    models.Base.metadata.create_all(DB_ENGINE)
    print "All models were synchronized!"
except:
    print "There was some problem in time to synchronize the database!"
