import asyncio
import socket
import threading
import json
import logging
import util

from typing import NewType, Optional, Tuple, List, Dict
from flask import Flask
from .models import User

# define Address to be 2-tuple of (host, port)
Address = NewType('Address', Tuple[str, int])


class ClientManager:
    """
    Keep track of currently conected clients.
    """

    class Client:
        """
        Data model for a connected client instance.
        """

        def __init__(self, patterns: List[str],
                     protocol: 'WebcandyServerProtocol'):
            self.patterns = patterns
            self.protocol = protocol

    clients: Dict[int, Client] = dict()  # map user_id to Client instance

    def __init__(self, app: Flask = None):
        self.app = app

    def init_app(self, app: Flask):
        self.app = app

    def register(self, token: str, patterns: List[str],
                 protocol: 'WebcandyServerProtocol') -> None:
        """
        Register a new client.

        :param token: authorization token provided by the client
        :param patterns: available patterns provided by the client
        :param protocol: ``WebcandyServerProtocol`` instance for the client
        :raises RuntimeError: if called before app is initialized
        """
        if not self.app:
            raise RuntimeError('app must be initialized to register client')

        with self.app.app_context():
            user: User = User.get_user(token)
            if user:
                protocol.user_id = user.id
                self.clients[user.id] = self.Client(patterns, protocol)
                logging.info(
                    f'Registered client {util.format_addr(protocol.peername)} '
                    f'with user {user.username!r}')

    # TODO: Add remove functionality

    def __getitem__(self, user_id):
        # TODO: Handle if website logged in user has no connected clients
        return self.clients[user_id]

    def __contains__(self, user_id):
        return user_id in self.clients


clients = ClientManager()  # make sure to call init_app on this


class WebcandyServerProtocol(asyncio.Protocol):
    """
    Protocol describing how data is sent and received with a client. Note that
    each client connection creates a new Protocol instance.
    """

    peername: Address = None
    transport: asyncio.Transport = None
    user_id: int = None  # this must be set

    def connection_made(self, transport: asyncio.Transport) -> None:
        """
        Handle an incoming connection. Do not register the client with a user
        until token data is received.
        """
        self.peername = transport.get_extra_info('peername')
        logging.info(f'Connected client {util.format_addr(self.peername)}')
        self.transport = transport

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.transport.close()
        # TODO: Remove from clients once functionality is implemented
        logging.info(f'Disconnected client {util.format_addr(self.peername)}')

    def data_received(self, data: bytes) -> None:
        """
        Attempt to parse access token and patterns out of received data. In
        practice, this callback should only be invoked upon initial client
        connection, though it should not error if this is not the case.
        """
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            logging.debug(f'Received text: {data.decode()!r} '
                          f'from {util.format_addr(self.peername)}')
            return

        try:
            token = parsed['token']
            patterns = parsed['patterns']
        except KeyError:
            logging.debug(f'Received JSON: {json.loads(data)} '
                          f'from {util.format_addr(self.peername)}')
            return

        logging.debug(f'Received patterns: {patterns} '
                      f'from {util.format_addr(self.peername)}')
        clients.register(token, patterns, self)

    def send(self, data: bytes) -> bool:
        """
        Send data to a client.
        :param data: the data to send
        :return: ``True`` if the operation was successful; ``False`` otherwise
        """
        try:
            self.transport.write(data)
        except AttributeError:
            logging.error('No client connection established')
            return False
        except OSError as e:
            logging.error(e)
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
        Start the proxy server.
        """

        async def _go():
            loop = asyncio.get_running_loop()
            server = await loop.create_server(
                WebcandyServerProtocol, '127.0.0.1', 6543)
            async with server:
                addr = server.sockets[0].getsockname()
                logging.info(f'Serving on {util.format_addr(addr)}')
                await server.serve_forever()

        if not self._server_running:
            # test if other instance is already running
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
                result = test_sock.connect_ex((self.host, self.port))

            if result == 10061:  # nothing running
                server_thread = threading.Thread(
                    target=lambda: asyncio.run(_go()))
                server_thread.start()
                self._server_running = True

    def send(self, user_id: int, data: bytes) -> bool:
        """
        Send data to the client associated with the specified user.

        :param user_id: ID of the user whose client to send data to
        :param data: the data to send
        :return: ``True`` if sending was successful; ``False`` otherwise
        """
        if not self._server_running:
            logging.error('Proxy server is not running')
            return False

        if user_id not in clients:
            logging.error(
                f'No clients associated with user_id {user_id}')
            return False

        clients[user_id].protocol.send(data)
        return True


proxy_server = ProxyServer()
