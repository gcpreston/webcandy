import asyncio
import socket
import threading
import json
import util

from typing import NewType, Dict, Tuple, Optional
from flask import Flask, g

# define Address to be 2-tuple of (host, port)
Address = NewType('Address', Tuple[str, int])

# IDEA
# - Keep track of Protocol instances associated with each client
#   * Maybe use a dict mapping client address to Protocol instance?
# - Call send method on proper Protocol instance to make send go through

# map username to client Protocol instance (assumes one client per user)
# TODO: Generalize to support multiple clients per user
CLIENTS: Dict[str, 'WebcandyServerProtocol'] = dict()


class WebcandyServerProtocol(asyncio.Protocol):
    """
    Protocol describing how data is sent and received with a client. Note
    that each client connection creates a new Protocol instance.
    """
    # TODO: Use app logger
    peername: Address = None
    transport: asyncio.Transport = None

    def connection_made(self, transport: asyncio.Transport) -> None:
        """
        Handle an incoming connection.
        """
        self.peername = transport.get_extra_info('peername')
        print(f'Connection made to {self.peername}')
        CLIENTS['testuser'] = self  # TODO: Register for a specified user
        self.transport = transport

    def connection_lost(self, exc: Optional[Exception]) -> None:
        del CLIENTS['testuser']

    def data_received(self, data: bytes) -> None:
        """
        Attempt to parse patterns out of received data. In practice, this
        callback should only be invoked upon initial client connection.
        """
        print(f'Incoming data from {self.peername}')

        try:
            patterns = json.loads(data)['patterns']
            print(f'Received patterns: {patterns}')
        except json.JSONDecodeError:
            print(f'Received text: {data.decode()!r}')
        except KeyError:
            print(f'Received JSON: {json.loads(data)}')

    def send(self, data: bytes) -> bool:
        """
        Send data to a client.
        :param data: the data to send
        :return: ``True`` if the operation was successful; ``False`` otherwise
        """
        try:
            self.transport.write(data)
        except AttributeError:
            print('No client connection established')
            return False
        except OSError as e:
            print(e)
            return False
        return True


class WebcandyClientManager:
    """
    Manage current open client connections.
    """
    _server_running: bool = False

    def __init__(self, app: Flask = None, host: str = '127.0.0.1',
                 port: int = 6543):
        self.app = app
        self.host = host
        self.port = port

    def init_app(self, app: Flask):
        self.app = app

    def start(self) -> None:
        """
        Start this Webcandy server.
        """

        async def _go():
            loop = asyncio.get_running_loop()
            server = await loop.create_server(
                WebcandyServerProtocol, '127.0.0.1', 6543)
            async with server:
                addr = server.sockets[0].getsockname()
                self.app.logger.info(f'Serving on {util.format_addr(addr)}')
                await server.serve_forever()

        if not self._server_running:
            # test if other instance is already running
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
                result = test_sock.connect_ex((self.host, self.port))

            if result == 10061:  # nothing running
                server_thread = threading.Thread(
                    target=lambda: asyncio.run(_go()))
                server_thread.start()

    def send(self, username: str, data: bytes) -> bool:
        """
        Send data to the client associated with the specified user.

        :param username: the user whose client to send data to
        :param data: the data to send
        :return: ``True`` if sending was successful; ``False`` otherwise
        """
        if username not in CLIENTS:
            self.app.logger.error(f'{username} has no associated clients')
            return False

        CLIENTS[username].send(data)
        return True
