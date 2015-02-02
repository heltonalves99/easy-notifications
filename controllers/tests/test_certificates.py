import unittest
from . import BaseTest


class TestCertificate(BaseTest):
    def test_access_denied(self):
        response = self.test_app.get('/api/certificates', expect_errors=True)
        self.assertEqual(response.status_int, 401)

    def test_access_granted(self):
        self.assertTrue(False)

    def test_certificates_response(self):
        self.assertTrue(False)

    def test_add_certificate(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
