import unittest
from app import main

from webtest import TestApp
from app.models import Base, db
from app.settings import DB_ENGINE


class BaseTest(unittest.TestCase):
    def setUp(self):
        # imports only to create_all sqlachemy method works :T
        from app.models.certificates import Certificate  # noqa
        from app.models.devices import Device  # noqa
        from app.models.users import User  # noqa

        self.test_app = TestApp(main)
        self.db = db
        Base.metadata.create_all(DB_ENGINE)

    def tearDown(self):
        Base.metadata.drop_all(DB_ENGINE)
