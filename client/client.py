import socket


class WebcandyClient:
    """
    Webcandy client to receive light configuration submission data from server.
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 6543):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        while True:
            data = self.s.recv(1024)
            if not data:
                continue
            print(data)


if __name__ == '__main__':
    client = WebcandyClient()
