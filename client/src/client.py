import asyncio
import json
import requests
import logging
import argparse

from controller import Controller
from fcserver import FadecandyServer


class WebcandyClientProtocol(asyncio.Protocol):
    """
    Protocol describing communication of a Webcandy client.
    """

    def __init__(self, access_token: str, control: Controller,
                 on_con_lost: asyncio.Future):
        self._token = access_token
        self._control = control
        self._on_con_lost = on_con_lost

    def connection_made(self, transport: asyncio.Transport) -> None:
        """
        When a connection is made, the send the server JSON data describing the
        patterns it has available.
        """
        data = json.dumps(
            {'token': self._token, 'patterns': ['test1', 'test2', 'test3']})
        transport.write(data.encode())
        logging.info(f'Data sent: {data}')

    def data_received(self, data: bytes) -> None:
        """
        Received data is assumed to be JSON describing a lighting configuration.
        Upon receiving data, attempt to decode it as JSON, and if successful,
        pass the parsed data to a ``Controller`` to attempt to run the described
        lighting configuration.
        """
        try:
            parsed = json.loads(data.decode())
            logging.debug(f'Received JSON: {parsed}')
            self._control.run(**parsed)
        except json.decoder.JSONDecodeError:
            logging.info(f'Received text: {data}')

    def connection_lost(self, exc) -> None:
        logging.info('The server closed the connection')
        self._on_con_lost.set_result(True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(
        description='Webcandy client to connect to a running Webcandy server.')
    parser.add_argument('username', help='the username to log in with')
    parser.add_argument('password', help='the password to log in with')
    parser.add_argument('--host', metavar='ADDRESS',
                        help='the address of the server to connect to'
                             '(default: 127.0.0.1)')
    parser.add_argument('--port', metavar='PORT', type=int,
                        help='the port the server is running on'
                             '(default: 6543)')
    cmd_args = parser.parse_args()

    cmd_host = cmd_args.host or '127.0.0.1'
    cmd_port = cmd_args.port or 6543

    # get access token from username and password
    response = requests.post(f'http://{cmd_host}:5000/api/token',
                             json={'username': cmd_args.username,
                                   'password': cmd_args.password})
    token = response.json()['token']

    # create and start Fadecandy server
    fc_server = FadecandyServer()
    fc_server.start()

    # set up WebcandyClientProtocol
    async def start_protocol():
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()

        transport, protocol = await loop.create_connection(
            lambda: WebcandyClientProtocol(token, Controller(), on_con_lost),
            cmd_host, cmd_port)

        # wait until the protocol signals that the connection is lost, then
        # close the transport stop the Fadecandy server
        try:
            await on_con_lost
        finally:
            transport.close()
            fc_server.stop()


    asyncio.run(start_protocol())
