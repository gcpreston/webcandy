import socket
import json


class WebcandyClient:
    """
    Webcandy client to receive light configuration submission data from server.
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 6543):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            while True:
                data = s.recv(1024)
                if data:
                    try:
                        parsed = json.loads(data)
                        print(f'Received json: {parsed}')
                    except json.decoder.JSONDecodeError:
                        print(f'Received text: {data}')


if __name__ == '__main__':
    client = WebcandyClient()
    client.start()
