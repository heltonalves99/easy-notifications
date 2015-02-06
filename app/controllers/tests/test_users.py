from . import BaseTest


class TestUser(BaseTest):
    def setUp(self):
        super(TestUser, self).setUp()
        self.base_url = '/api/users'

    def test_create_and_authenticate_user(self):
        user = {
            'username': 'john',
            'email': 'johmail@foobar.com',
            'password': 'password'
        }
        response = self.test_app.post(self.base_url, user, expect_errors=True)
        self.assertEqual(response.status_int, 200)

        self.test_app.authorization = ('Basic', ('john', 'password'))
        response = self.test_app.get('/api/certificates', expect_errors=True)
        self.assertEqual(response.status_int, 200)
