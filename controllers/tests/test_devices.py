import unittest

from passlib.hash import sha256_crypt
from models.users import User
from . import BaseTest


class TestDevice(BaseTest):
    def setUp(self):
        super(TestDevice, self).setUp()

        self.user1 = User(
            username="john",
            email="johmail@foobar.com",
            password=sha256_crypt.encrypt("password")
        )

        self.user2 = User(
            username="max",
            email="maxmail@foobar.com",
            password=sha256_crypt.encrypt("password")
        )

        self.db.add(self.user1)
        self.db.add(self.user2)
        self.db.commit()

    def _auth(self):
        self.test_app.authorization = ('Basic', ('john', 'password'))

    def _auth2(self):
        self.test_app.authorization = ('Basic', ('max', 'password'))

    def test_access_denied(self):
        self.test_app.authorization = ('Basic', ('john', 'password-wrong'))
        response = self.test_app.get('/api/devices', expect_errors=True)
        self.assertEqual(response.status_int, 401)

    def test_access_granted(self):
        self._auth()
        response = self.test_app.get('/api/devices', expect_errors=True)
        self.assertEqual(response.status_int, 200)

    def test_empty_json_response(self):
        self._auth()
        response = self.test_app.get('/api/devices', expect_errors=True)
        empty_json = {'results': []}
        self.assertEqual(response.json, empty_json)


if __name__ == '__main__':
    unittest.main()
