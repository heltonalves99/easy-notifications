import os
import unittest
import app

from webtest import TestApp
from plugins import sql_plugin
from models import Base, test_engine


class BaseTest(unittest.TestCase):
    def setUp(self):
        # imports only to create_all sqlachemy method works :T
        from models.certificates import Certificate  # noqa
        from models.devices import Device  # noqa
        from models.users import User  # noqa

        app.main.uninstall('sqlalchemy')
        app.main.install(sql_plugin(test=True))
        self.test_app = TestApp(app.main)
        Base.metadata.create_all(test_engine)

    def tearDown(self):
        db_file = os.path.abspath('test_database.sqlite3')
        os.remove(db_file)
