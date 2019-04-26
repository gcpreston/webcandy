import asyncio
import json
import argparse

from controller import Controller


class WebcandyClient:
    """
    Webcandy client to receive light configuration submission data from server.
    """

    def __init__(self, control: Controller, host: str, port: int):
        self.control = control
        self.host = host
        self.port = port

    def start(self):
        """
        Connect to the specified Webcandy server and start receiving data.
        """

        async def _start():
            reader, writer = await asyncio.open_connection(self.host, self.port)
            print(f'Connected to server {self.host}:{self.port}')

            while True:
                try:
                    data = await reader.read(100)
                    try:
                        parsed = json.loads(data.decode())
                        print(f'Received JSON: {parsed}')
                        self.control.run_script(**parsed)
                    except json.decoder.JSONDecodeError:
                        print(f'Received text: {data}')
                except KeyboardInterrupt:
                    break

            writer.close()
            print('Connecton closed')
            await writer.wait_closed()

        asyncio.run(_start())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Webcandy client to connect to a running Webcandy server.')
    parser.add_argument('--host', metavar='ADDRESS',
                        help='the address of the server to connect to'
                             '(default: 127.0.0.1)')
    parser.add_argument('--port', metavar='PORT', type=int,
                        help='the port the server is running on'
                             '(default: 6543)')
    cmd_args = parser.parse_args()

    host = cmd_args.host or '127.0.0.1'
    port = cmd_args.port or 6543

    client = WebcandyClient(Controller(), host, port)
    client.start()
