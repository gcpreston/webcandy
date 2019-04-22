import unittest
import json

from webcandy.app import create_app


class TestAPI(unittest.TestCase):
    """
    Test API routes.
    """

    def setUp(self) -> None:
        """
        Initialize API tests by retrieving an access token.
        """
        self.app = create_app().test_client()
        # this tests the /api/token route
        self.token = self.login('testuser', 'Webcandy1')

    def login(self, username: str, password: str) -> str:
        """
        Log in to Webcandy and retrieve an access token.

        :param username: the username to log in with
        :param password: the password to log in with
        :return: the access token
        """
        response = self.app.post('/api/token', json={'username': username,
                                                     'password': password})
        return json.loads(response.get_data())['token']

    def get(self, route: str, token: str = None):
        """
        Perform a GET request.

        :param route: the path to GET
        :param token: an API token, if one is required
        :return: the response
        """
        headers = dict()
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return self.app.get(route, headers=headers)

    def test_patterns(self):
        """
        Test the /patterns URI.
        """
        response = self.get('/api/patterns')  # authorization not needed
        self.assertEqual(json.loads(response.get_data()),
                         ['fade', 'scroll', 'solid_color'])

    def test_colors(self):
        """
        Test the /colors URI.
        """
        response = self.get('/api/colors', self.token)
        self.assertEqual(json.loads(response.get_data()),
                         {
                             "blue": "#4169e1",
                             "green": "#00ff80",
                             "pink": "#ff69b4",
                             "purple": "#8a2be2",
                             "yellow": "#ffff99"
                         })

    def test_color_lists(self):
        """
        Test the /color-lists URI.
        """
        response = self.get('/api/color-lists', self.token)
        self.assertEqual(json.loads(response.get_data()),
                         {
                             "default": [
                                 "#ff0000",
                                 "#ff7f00",
                                 "#ffff00",
                                 "#00ff00",
                                 "#0000ff",
                                 "#8b00ff"
                             ]
                         })
