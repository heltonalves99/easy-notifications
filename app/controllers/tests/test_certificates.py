from passlib.hash import sha256_crypt
from app.models.certificates import Certificate
from app.models.users import User
from . import BaseTest


class TestCertificate(BaseTest):
    def setUp(self):
        super(TestCertificate, self).setUp()

        self.base_url = '/api/certificates'

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
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 401)

    def test_access_granted(self):
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(response.status_int, 200)

    def test_empty_json_response(self):
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(response.json['results'], [])

    def test_manual_add_certificates(self):
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 0)
        cert1 = Certificate(
            name='my-cert',
            platform='ios',
            type='sandbox',
            cert_pem='cert',
            key_pem='key',
            user=self.user1
        )
        self.db.add(cert1)
        self.db.commit()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 1)

    def test_api_add_certificates(self):
        self._auth()

        cert = {
            'name': 'my-cert',
            'platform': 'ios',
            'type': 'sandbox',
            'cert_pem': 'cert',
            'key_pem': 'key'
        }

        response = self.test_app.post(self.base_url, cert, expect_errors=True)
        cert['user_id'] = self.user1.id
        cert['token'] = response.json['token']
        self.assertEqual(response.json, cert)

    def test_filter_by_user(self):
        # inserting certificate to user1
        self._auth()
        cert = {
            'name': 'my-cert',
            'platform': 'ios',
            'type': 'sandbox',
            'cert_pem': 'cert',
            'key_pem': 'key'
        }
        response = self.test_app.post(self.base_url, cert, expect_errors=True)

        # verifying if user2 sees the certificate
        self._auth2()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 0)

        # verifying if user1 sees the certificate
        self._auth()
        response = self.test_app.get(self.base_url, expect_errors=True)
        self.assertEqual(len(response.json['results']), 1)
