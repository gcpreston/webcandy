import unittest

from webcandy.server import ClientManager


class TestClientManager(unittest.TestCase):
    """
    Tests for ClientManager class.
    """

    def test_register(self):
        manager = ClientManager()
        # assert that RuntimeError is raised when app isn't initialized
        self.assertRaises(RuntimeError, manager.register,
                          'some-token', [], None)
