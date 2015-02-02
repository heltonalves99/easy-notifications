import unittest

from passlib.hash import sha256_crypt
from models.certificates import Certificate
from models.devices import Device
from models.users import User
from . import BaseTest


class TestDevice(BaseTest):
    def setUp(self):
        super(TestDevice, self).setUp()
        self.base_url = '/api/devices'
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

        self.cert1 = Certificate(
            name='my-cert',
            platform='ios',
            type='sandbox',
            cert_pem='cert',
            key_pem='key',
            user=self.user1
        )

        self.db.add(self.user1)
        self.db.add(self.user2)
        self.db.add(self.cert1)
        self.db.commit()

    def _auth(self):
        self.test_app.authorization = ('Basic', ('john', 'password'))

    def _auth2(self):
        self.test_app.authorization = ('Basic', ('max', 'password'))

    def test_access_denied(self):
        self.test_app.authorization = ('Basic', ('john', 'password-wrong'))
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 401)

    def test_access_granted(self):
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 200)

    def test_empty_json_response(self):
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        empty_json = {'results': []}
        self.assertEqual(response.json, empty_json)

    def test_manual_add_devices(self):
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 0)
        device = Device(
            name='my-device',
            token='device-token',
            status=True,
            certificate=self.cert1
        )
        self.db.add(device)
        self.db.commit()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 1)

    def test_api_add_devices(self):
        self._auth()

        device = {
            'name': 'my-device',
            'token': 'device-token',
            'status': True,
            'certificate': self.cert1.id
        }

        response = self.test_app.post(self.base_url, device, expect_errors=True)
        device.pop('certificate')
        device['certificate_id'] = self.cert1.id
        self.assertEqual(response.json, device)

    def test_filter_by_user(self):
        # inserting certificate to user1
        self._auth()

        device = {
            'name': 'my-device',
            'token': 'device-token',
            'status': True,
            'certificate': self.cert1.id
        }

        response = self.test_app.post(self.base_url, device, expect_errors=True)

        # verifying if user2 sees the certificate
        self._auth2()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 0)

        # verifying if user1 sees the certificate
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 1)

if __name__ == '__main__':
    unittest.main()
