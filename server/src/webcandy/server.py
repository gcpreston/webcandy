import asyncio
import socket
import threading
import json
import util

from typing import NewType, Tuple, Optional
from flask import Flask
from .models import User

# IDEA
# - Keep track of Protocol instances associated with each client
#   * Maybe use a dict mapping client address to Protocol instance?
# - Call send method on proper Protocol instance to make send go through

# define Address to be 2-tuple of (host, port)
Address = NewType('Address', Tuple[str, int])


class ClientManager:
    """
    Map a username to ``WebcandyServerProtocol`` instance. Used for ensuring
    authentication and calling ``init_app`` on each protocol automatically.
    Does not subclass ``dict`` due to requiring a token upon setting value.
    """
    # TODO: Subclass some kind of dict
    # TODO: Enforce that app is initialized
    # TODO: Generalize to support multiple clients per user

    def __init__(self, app: Flask = None):
        self.app = app
        self.data = dict()

    def init_app(self, app: Flask):
        self.app = app

    def get(self, key):
        return self.__getitem__(key)

    def set(self, token: str, value: 'WebcandyServerProtocol'):
        with self.app.app_context():
            user: User = User.get_user(token)  # TODO: Handle exceptions
            value.init_app(self.app)  # TODO: Handle exceptions?
            self.data[user.id] = value

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        del self.data['key']

    def __contains__(self, item):
        return item in self.data


manager = ClientManager()  # TODO: Move somewhere else


class WebcandyServerProtocol(asyncio.Protocol):
    """
    Protocol describing how data is sent and received with a client. Note
    that each client connection creates a new Protocol instance.
    """
    # TODO: Use app logger
    peername: Address = None
    transport: asyncio.Transport = None
    app = None

    def init_app(self, app: Flask):
        """
        Associate this ``WebcandyServerProtocol`` with a Flask application. This
        must be called before the protocol is used for authentication and
        logging capabilities.
        :param app: the Flask app to associate
        """
        self.app = app

    def connection_made(self, transport: asyncio.Transport) -> None:
        """
        Handle an incoming connection. Do not register the client with a user
        until token data is received.
        """
        self.peername = transport.get_extra_info('peername')
        print(f'Connection made to {self.peername}')
        self.transport = transport

    def connection_lost(self, exc: Optional[Exception]) -> None:
        del manager['testuser']

    def data_received(self, data: bytes) -> None:
        """
        Attempt to parse access token and patterns out of received data. In
        practice, this callback should only be invoked upon initial client
        connection, though it should not error if this is not the case.
        """
        print(f'Incoming data from {self.peername}')

        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            print(f'Received text: {data.decode()!r}')
            return

        try:
            token = parsed['token']
            patterns = parsed['patterns']
        except KeyError:
            print(f'Received JSON: {json.loads(data)}')
            return

        print(f'Received patterns: {patterns}')
        manager.set(token, self)

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


class ProxyServer:
    """
    Manage running a server implementing ``WebcandyServerProtocol``.
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

    def send(self, user_id: int, data: bytes) -> bool:
        """
        Send data to the client associated with the specified user.

        :param user_id: ID of the user whose client to send data to
        :param data: the data to send
        :return: ``True`` if sending was successful; ``False`` otherwise
        """
        if user_id not in manager:
            self.app.logger.error(f'User {user_id} has no associated clients')
            return False

        manager[user_id].send(data)
        return True
