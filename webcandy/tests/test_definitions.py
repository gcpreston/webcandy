import unittest
import os

from webcandy.definitions import ROOT_DIR, DATA_DIR, USERS_DIR, STATIC_DIR


class TestDefinitions(unittest.TestCase):
    """
    Tests for ``definitions`` module.
    """

    def test_root_dir(self):
        """
        ROOT_DIR should point to the webcandy package.
        """
        root = os.listdir(ROOT_DIR)
        for item in {'__init__.py', 'app.py'}:
            self.assertTrue(item in root)

    def test_data_dir(self):
        """
        DATA_DIR is where the users directory should live.
        """
        self.assertTrue('users' in os.listdir(DATA_DIR))

    def test_users_dir(self):
        """
        USERS_DIR should only contain JSON files.
        """
        for f in os.listdir(USERS_DIR):
            self.assertTrue(f.endswith('.json'))

    def test_static_dir(self):
        """
        STATIC_DIR is where index.html should live.
        """
        self.assertTrue('index.html' in os.listdir(STATIC_DIR))
