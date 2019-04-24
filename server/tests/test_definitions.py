import unittest
import os

from definitions import ROOT_DIR


class TestDefinitions(unittest.TestCase):

    def test_root_dir(self):
        # ROOT_DIR points to correct location
        for folder in {'bin', 'server', 'static'}:
            self.assertTrue(folder in os.listdir(ROOT_DIR))
