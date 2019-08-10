import unittest
import json

from webcandy.app import create_app


class TestAPI(unittest.TestCase):
    """
    Test API routes.
    """
    app = create_app(False).test_client()
    token: str

    def setUp(self) -> None:
        # this tests the /api/token route
        self.token = self.retrieve_token('testuser1', 'Webcandy1')

    def retrieve_token(self, username: str, password: str) -> str:
        """
        Log in to Webcandy and retrieve an access token.

        :param username: the username to log in with
        :param password: the password to log in with
        :return: the access token
        """
        response = self.app.post('/api/token', json={'username': username,
                                                     'password': password})
        data = response.get_data()
        data_json = json.loads(data)
        return data_json['token']

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

    # TODO: Test PUT on colors and color_lists

    def test_user_clients(self):
        """
        Test the /api/user/clients URI.
        """
        # test no connected clients
        response = self.get('/api/user/clients', self.token)
        self.assertListEqual(json.loads(response.get_data()), [])
        # TODO: Simulate clients and finish /api/user/clients test

    def test_user_info(self):
        """
        Test the /api/user/info URI.
        """
        response = self.get('/api/user/info', self.token)
        self.assertDictEqual(json.loads(response.get_data()),
                             {
                                 'user_id': 1,
                                 'username': 'testuser1',
                                 'email': 'testuser1@email.com'

                             })

    def test_user_data(self):
        """
        Test the /color_lists URI.
        """
        response = self.get('/api/user/data', self.token)
        self.assertEqual(json.loads(response.get_data()),
                         {
                             'colors': {
                                 "blue": "#4169e1",
                                 "green": "#00ff80",
                                 "pink": "#ff69b4",
                                 "purple": "#8a2be2",
                                 "yellow": "#ffff99"
                             },
                             'color_lists': {
                                 "rainbow": [
                                     "#ff0000",
                                     "#ff7f00",
                                     "#ffff00",
                                     "#00ff00",
                                     "#0000ff",
                                     "#8b00ff"
                                 ]
                             }
                         })
