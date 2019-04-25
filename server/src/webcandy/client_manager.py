import socket
import threading

from flask import Flask


class WebcandyClientManager:
    """
    Class to manage client socket connections.
    """

    conn = None

    def __init__(self, app: Flask = None, host: str = '127.0.0.1',
                 port: int = 6543):
        self.app = app
        self.host = host
        self.port = port

    def init_app(self, app):
        self.app = app

    def start(self):
        # test if manager is already running
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
            result = test_sock.connect_ex((self.host, self.port))

        if result == 10061:  # nothing running
            thread = threading.Thread(target=_connect, args=(self,))
            thread.start()
            thread.join()

    def send(self, data: bytes) -> bool:
        """
        Send data to a client.
        :param data: the data to send
        :return: ``True`` if the operation was successful; ``False`` otherwise
        """
        try:
            self.conn.sendall(data)
        except AttributeError:
            self.app.logger.error('No client connection established')
            return False
        except OSError as e:
            self.app.logger.error(e)
            return False
        return True


def _connect(manager: WebcandyClientManager):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((manager.host, manager.port))
        s.listen()

        # while True:
        conn, addr = s.accept()
        manager.app.logger.debug(f'Connected {addr}')
        manager.conn = conn
