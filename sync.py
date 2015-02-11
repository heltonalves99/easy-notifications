from app.models.users import User  # noqa
from app.models.devices import Device  # noqa
from app.models.certificates import Certificate  # noqa
from app import models

try:
    models.Base.metadata.create_all(models.prod_engine)
    print "All models were synchronized!"
except:
    print "There was some problem in time to synchronize the database!"
