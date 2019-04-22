import unittest
import json

from webcandy.app import create_app


class TestAPI(unittest.TestCase):
    """
    Test API routes.
    """

    app = create_app().test_client()

    def login(self, username: str, password: str):
        """
        Log in to Webcandy and retrieve an access token.
        :param username: the username to log in with
        :param password: the password to log in with
        """
        response = self.app.post('/api/token', json={'username': username,
                                                     'password': password})
        return json.loads(response.get_data())['token']

    def test_token(self):
        """
        Test the /api/token route.
        """
        token = self.login('testuser', 'Webcandy1')
        self.assertTrue(token)
