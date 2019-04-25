import socket
import multiprocessing
import logging


def _accept_connections(sock: socket.socket):
    while True:
        conn, addr = sock.accept()
        with conn:
            print(f'Connected {addr}')
            conn.sendall(b'Hello client!')


class WebcandyClientManager:
    """
    Class to manage client socket connections.
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 6543):
        # test if manager is already running
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
            result = test_sock.connect_ex((host, port))

        if result == 10061:  # nothing running
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((host, port))
                sock.listen()
                # p = multiprocessing.Process(target=_accept_connections,
                #                             args=(sock,))
                # p.start()
                self.conn, self.addr = sock.accept()

    def send(self, data: bytes) -> bool:
        try:
            self.conn.sendall(data)
        except OSError as e:
            logging.error(e)
            return False
        return True
