import unittest
import os

from webcandy.definitions import ROOT_DIR, DATA_DIR, STATIC_DIR


class TestDefinitions(unittest.TestCase):
    """
    Tests for ``definitions`` module.
    """

    def test_root_dir(self):
        """
        ROOT_DIR should point to the project root.
        """
        root = os.listdir(ROOT_DIR)
        for item in {'webcandy', 'setup.py'}:
            self.assertTrue(item in root)

    def test_data_dir(self):
        """
        DATA_DIR should only contain JSON files.
        """
        for f in os.listdir(DATA_DIR):
            self.assertTrue(f.endswith('.json'))

    def test_static_dir(self):
        """
        STATIC_DIR should contain index.html at the very least.
        """
        self.assertTrue('index.html' in os.listdir(STATIC_DIR))
