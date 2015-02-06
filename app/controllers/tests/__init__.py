import unittest
from app import main

from webtest import TestApp
from app.models import Base, test_engine, session


class BaseTest(unittest.TestCase):
    def setUp(self):
        # imports only to create_all sqlachemy method works :T
        from app.models.certificates import Certificate  # noqa
        from app.models.devices import Device  # noqa
        from app.models.users import User  # noqa

        self.test_app = TestApp(main)
        self.db = session()
        Base.metadata.create_all(test_engine)

    def tearDown(self):
        Base.metadata.drop_all(test_engine)
