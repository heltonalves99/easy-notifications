import json
from passlib.hash import sha256_crypt
from app.models.users import User
from app.models.devices import Device
from app.models.certificates import Certificate
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

        self.cert1 = Certificate(
            name='my-cert',
            platform='ios',
            type='sandbox',
            cert_pem='cert',
            key_pem='key',
            user=self.user1
        )

        self.db.add(self.user1)
        self.db.add(self.cert1)
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

    def test_payload_must_be_valid_dict(self):
        self._auth()

        device = Device(
            name='my-device',
            token='device-token',
            status=True,
            certificate=self.cert1
        )
        self.db.add(device)
        self.db.commit()

        data = {
            'tokens': ['device-token'],
            'payload': '{non-valid-json}'
        }

        response = self.test_app.post(self.base_url, data, expect_errors=True)
        self.assertEqual(response.json, {'error': ['Payload must be a valid json.']})

    def test_tokens_need_at_least_one_item(self):
        self._auth()
        payload = {'abc': 123}

        data = {
            'tokens': [],
            'payload': json.dumps(payload)
        }

        response = self.test_app.post(self.base_url, data, expect_errors=True)
        self.assertEqual(response.json, {'error': ['Tokens need at least one item.']})

    def test_need_return_error_list(self):
        self._auth()
        error_list = ['Payload must be a valid json.',
                      'Tokens need at least one item.']
        data = {
            'tokens': [],
            'payload': '{non-valid-json}'
        }

        response = self.test_app.post(self.base_url, data, expect_errors=True)
        self.assertEqual(response.json, {'error': error_list})

    def test_get_devices_to_push(self):
        self._auth()

        device = Device(
            name='my-device',
            token='device-token',
            status=True,
            certificate=self.cert1
        )
        self.db.add(device)
        self.db.commit()

        payload = {'abc': 123}
        data = {
            'tokens': ['device-token'],
            'payload': json.dumps(payload)
        }

        response = self.test_app.post(self.base_url, data, expect_errors=True)
        self.assertEqual(response.json, {'message': 'Push notification delivered.',
                                         'devices': [1]})
