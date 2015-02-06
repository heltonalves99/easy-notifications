from passlib.hash import sha256_crypt
from models.users import User
from . import BaseTest


class TestNotification(BaseTest):
    def setUp(self):
        super(TestNotification, self).setUp()

        self.base_url = '/api/notifications'

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
        response = self.test_app.post(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 401)

    def test_access_granted(self):
        self._auth()
        response = self.test_app.post(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 200)

    def test_receiving_valid_dict(self):
        self._auth()

        data = {
            'tokens': ['abc123', 'abcdef'],
            'payload': '{non-valid-json}'
        }

        response = self.test_app.post(self.base_url, data, expect_errors=True)
        self.assertEqual(response.json, {'error': 'Payload must be a valid json.'})
