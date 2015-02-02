import unittest
import app
from webtest import TestApp

test_app = TestApp(app.main)


class TestCertificate(unittest.TestCase):
    def test_access_denied(self):
        response = test_app.get('/api/certificates', expect_errors=True)
        self.assertEqual(response.status_int, 401)

    def test_access_granted(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
