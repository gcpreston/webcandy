import asyncio
import json
import logging
import argparse

from controller import Controller
from fcserver import FadecandyServer


class WebcandyClientProtocol(asyncio.Protocol):
    """
    Protocol describing communication of a Webcandy client.

    When a connection is made, the client sends the server JSON data describing
    the patterns it has available.

    Received data is assumed to be JSON describing a lighting configuration.
    Upon receiving data, the client attempts to decode it as JSON, and if
    successful, passes the parsed data to a ``Controller`` to attempt to run
    the described lighting configuration.
    """

    def __init__(self, control: Controller, on_con_lost: asyncio.Future):
        self.control = control
        self.on_con_lost = on_con_lost

    def connection_made(self, transport) -> None:
        patterns = json.dumps({'patterns': ['test1', 'test2', 'test3']})
        transport.write(patterns.encode())
        logging.info(f'Data sent: {patterns}')

    def data_received(self, data):
        try:
            parsed = json.loads(data.decode())
            logging.debug(f'Received JSON: {parsed}')
            self.control.run(**parsed)
        except json.decoder.JSONDecodeError:
            logging.info(f'Received text: {data}')

    def connection_lost(self, exc):
        logging.info('The server closed the connection')
        self.on_con_lost.set_result(True)


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

    # create and start Fadecandy server
    fc_server = FadecandyServer()
    fc_server.start()

    # set up WebcandyClientProtocol
    async def start_protocol():
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()

        transport, protocol = await loop.create_connection(
            lambda: WebcandyClientProtocol(Controller(), on_con_lost),
            cmd_host, cmd_port)

        # wait until the protocol signals that the connection is lost, then
        # close the transport stop the Fadecandy server
        try:
            await on_con_lost
        finally:
            transport.close()
            fc_server.stop()

    asyncio.run(start_protocol())
