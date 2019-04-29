import asyncio
import json
import logging
import argparse

from controller import Controller
from fcserver import FadecandyServer


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
            logging.info(f'Connected to server {self.host}:{self.port}')

            # TODO: Send server available patterns

            while True:
                try:
                    data = await reader.read(1024)
                    if data:
                        try:
                            parsed = json.loads(data.decode())
                            logging.debug(f'Received JSON: {parsed}')
                            self.control.run(**parsed)
                        except json.decoder.JSONDecodeError:
                            logging.info(f'Received text: {data}')
                except KeyboardInterrupt:
                    break

            writer.close()
            logging.info('Connecton closed')
            await writer.wait_closed()

        asyncio.run(_start())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(
        description='Webcandy client to connect to a running Webcandy server.')
    parser.add_argument('--host', metavar='ADDRESS',
                        help='the address of the server to connect to'
                             '(default: 127.0.0.1)')
    parser.add_argument('--port', metavar='PORT', type=int,
                        help='the port the server is running on'
                             '(default: 6543)')
    cmd_args = parser.parse_args()

    cmd_host = cmd_args.host or '127.0.0.1'
    cmd_port = cmd_args.port or 6543

    # create Fadecandy server and Webcandy client
    server = FadecandyServer()
    client = WebcandyClient(Controller(), cmd_host, cmd_port)

    # start processes
    server.start()
    client.start()
