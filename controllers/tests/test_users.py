import unittest

from passlib.hash import sha256_crypt
from models.certificates import Certificate
from models.devices import Device
from models.users import User
from . import BaseTest


class TestUser(BaseTest):
    def setUp(self):
        super(TestUser, self).setUp()
        self.base_url = '/api/devices'
        self.user1 = User(
            username="john",
            email="johmail@foobar.com",
            password=sha256_crypt.encrypt("password")
        )

        self.db.add(self.user1)
        self.db.commit()

    def _auth(self):
        self.test_app.authorization = ('Basic', ('john', 'password'))

    def test_access_denied(self):
        self.test_app.authorization = ('Basic', ('john', 'password-wrong'))
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 401)

    def test_access_granted(self):
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 200)
