from . import BaseTest


class TestUser(BaseTest):
    def setUp(self):
        super(TestUser, self).setUp()
        self.base_url = '/api/users'

        self.user = {
            'username': 'john',
            'email': 'johmail@foobar.com',
            'password': 'password'
        }

    def test_create_and_authenticate_user(self):

        response = self.test_app.post(self.base_url, self.user, expect_errors=True)
        self.assertEqual(response.status_int, 200)

        self.test_app.authorization = ('Basic', ('john', 'password'))
        response = self.test_app.get('/api/certificates', expect_errors=True)
        self.assertEqual(response.status_int, 200)

    def test_verify_exist_user_registered(self):
        self.test_app.post(self.base_url, self.user, expect_errors=True)

        self.user['username'] = 'smith'

        response = self.test_app.post(self.base_url, self.user, expect_errors=True)
        self.assertEqual(response.status_int, 400)

        self.user['username'] = 'john'
        self.user['email'] = 'smithmail@foobar.com'

        response = self.test_app.post(self.base_url, self.user, expect_errors=True)
        self.assertEqual(response.status_int, 400)
