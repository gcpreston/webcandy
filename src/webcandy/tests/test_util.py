import unittest
from webcandy import util


class TestUtil(unittest.TestCase):
    """
    Tests for ``util`` module.
    """

    def test_load_user_data(self):
        # User "testfakeuser" does not exist
        self.assertRaises(ValueError, util.load_user_data, 'testfakeuser')
        self.assertTrue(util.load_user_data(1))  # testuser1

    def test_format_error(self):
        self.assertEqual(util.format_error(5050, 'Some description'),
                         {'error': '(undefined)',
                          'error_description': 'Some description'})
        self.assertEqual(util.format_error(400, 'Bad Request test'),
                         {'error': 'Bad Request',
                          'error_description': 'Bad Request test'})
        self.assertEqual(util.format_error(401, 'Unauthorized test'),
                         {'error': 'Unauthorized',
                          'error_description': 'Unauthorized test'})
        self.assertEqual(util.format_error(404, 'Not Found test'),
                         {'error': 'Not Found',
                          'error_description': 'Not Found test'})
