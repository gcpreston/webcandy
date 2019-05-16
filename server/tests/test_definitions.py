import unittest
import os

from webcandy.definitions import ROOT_DIR, DATA_DIR


class TestDefinitions(unittest.TestCase):
    """
    Tests for ``definitions`` module.
    """

    def test_root_dir(self):
        """
        ROOT_DIR should point to the project root.
        """
        for folder in {'server', 'static'}:
            self.assertTrue(folder in os.listdir(ROOT_DIR))

    def test_data_dir(self):
        """
        DATA_DIR should only contain JSON files.
        """
        for f in os.listdir(DATA_DIR):
            self.assertTrue(f.endswith('.json'))
