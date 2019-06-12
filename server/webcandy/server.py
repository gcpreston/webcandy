import asyncio
import socket
import threading
import json
import logging

from collections import defaultdict
from typing import NewType, Optional, Tuple, List, Dict
from flask import Flask
from . import util
from .config import configure_logger
from .models import User

# define Address to be 2-tuple of (host, port)
Address = NewType('Address', Tuple[str, int])

# define module logger since app isn't initialized when this is run
logger = logging.getLogger(__name__)
configure_logger(logger)


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

    # map user_id to map of client ID to Client instance
    clients: Dict[int, Dict[str, Client]] = defaultdict(dict)

    def __init__(self, app: Flask = None):
        self.app = app

    def init_app(self, app: Flask):
        self.app = app

    def register(self, token: str, client_id: str, patterns: List[str],
                 protocol: 'WebcandyServerProtocol') -> None:
        """
        Register a new client.

        :param token: authorization token provided by the client
        :param client_id: the client ID to use; must be unique for this user
        :param patterns: available patterns provided by the client
        :param protocol: ``WebcandyServerProtocol`` instance for the client
        :raises RuntimeError: if called before app is initialized
        """
        if not self.app:
            raise RuntimeError('app must be initialized to register client')

        with self.app.app_context():
            user: User = User.get_user(token)
            if user:
                protocol.init(user.user_id, client_id)
                self.clients[user.user_id][client_id] = self.Client(patterns,
                                                                    protocol)
                logger.info(
                    f'Registered client {client_id!r} '
                    f'with user {user.user_id}')
            else:
                logger.error(f'No user could be associated with token {token!r}'
                             f' from {util.format_addr(protocol.peername)}')
                protocol.transport.write(b'Invalid authentication token.\n')
                protocol.transport.close()

    def remove(self, user_id: int, client_id: str) -> None:
        """
        Close a client's transport and remove it from the client manager.

        :param user_id: the user who owns the client
        :param client_id: the ID of the client to remove
        :raises ValueError: if user has no associated clients
        """
        if not self.contains(user_id, client_id):
            raise ValueError(f'User {user_id} has no associated client with ID '
                             f'{client_id!r}')

        self.clients[user_id][client_id].protocol.transport.close()
        del self.clients[user_id][client_id]

    def available_clients(self, user_id: int) -> List[str]:
        """
        Get a list of IDs of currently connected clients.
        """
        return list(self.clients[user_id])

    def get(self, user_id: int, client_id: str) -> Client:
        """
        Get a currently registered client.
        """
        return self.clients[user_id][client_id]

    def contains(self, user_id: int, client_id: str):
        """
        Check if a user has a client with the specified ID.
        """
        return client_id in self.clients[user_id]


clients = ClientManager()  # make sure to call init_app on this


class WebcandyServerProtocol(asyncio.Protocol):
    """
    Protocol describing how data is sent and received with a client. Note that
    each client connection creates a new Protocol instance.
    """

    peername: Address = None
    transport: asyncio.Transport = None

    # these must be set
    user_id: int = None
    client_id: str = None

    def init(self, user_id: int, client_id: str):
        """
        Set required fields for this protocol.

        :param user_id: the user owning the client this protocol represents
        :param client_id: the ID of the client this protocol represents
        """
        self.user_id = user_id
        self.client_id = client_id

    def connection_made(self, transport: asyncio.Transport) -> None:
        """
        Handle an incoming connection. Do not register the client with a user
        until required data is recieved (token, client_id, and patterns).
        """
        self.peername = transport.get_extra_info('peername')
        logger.info(f'Connected client {util.format_addr(self.peername)}')
        self.transport = transport

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if self.user_id and clients.contains(self.user_id, self.client_id):
            clients.remove(self.user_id, self.client_id)
        logger.info(f'Disconnected user {self.user_id}, '
                    f'client {self.client_id!r} '
                    f'({util.format_addr(self.peername)})')

    def data_received(self, data: bytes) -> None:
        """
        Attempt to parse access token and patterns out of received data. In
        practice, this callback should only be invoked upon initial client
        connection, though it should not error if this is not the case.
        """
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            logger.info(f'Received text: {data.decode()!r} '
                        f'from {util.format_addr(self.peername)}')
            return

        token = parsed.get('token')
        client_id = parsed.get('client_id')
        patterns = parsed.get('patterns')

        if token is None:
            logger.error('Missing token in data from '
                         f'{util.format_addr(self.peername)}')
            self.transport.write(b"[ERROR] Please provide an authentication "
                                 b"token in a 'token' field.\n")
            self.transport.close()
            return
        if client_id is None:
            logger.error('Missing client_id in data from '
                         f'{util.format_addr(self.peername)}')
            self.transport.write(b"[ERROR] Please provide a client ID in a "
                                 b"'client_id' field.\n")
            self.transport.close()
            return
        if patterns is None:
            logger.error('Missing patterns in data from '
                         f'{util.format_addr(self.peername)}')
            self.transport.write(b"[ERROR] Please provide the client's "
                                 b"available patterns in a 'patterns' field.\n")
            self.transport.close()
            return

        clients.register(token, client_id, patterns, self)

    def send(self, data: dict) -> bool:
        """
        Send dictionary data to a client.
        :param data: the data to send
        :return: ``True`` if the operation was successful; ``False`` otherwise
        """
        try:
            self.transport.write(bytes(json.dumps(data), 'utf-8'))
        except AttributeError:
            logger.error('No client connection established')
            return False
        except OSError as e:
            logger.error(e)
            return False
        return True


class ProxyServer:
    """
    Manage running a server implementing ``WebcandyServerProtocol``.
    """
    _server_running: bool = False

    # TODO: Make proxy server host/port configurable within app context
    def start(self, host: str = '127.0.0.1', port: int = 6543) -> None:
        """
        Start the proxy server.

        :param host: the host to serve on
        :param port: the port to serve on
        """

        async def _go():
            loop = asyncio.get_running_loop()
            server = await loop.create_server(
                WebcandyServerProtocol, host, port)
            async with server:
                addr = server.sockets[0].getsockname()
                logger.info(f'Proxy server bound to {util.format_addr(addr)}')
                await server.serve_forever()

        if not self._server_running:
            # test if other instance is already running
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
                status = test_sock.connect_ex((host, port))

            if status in {10061, 111}:  # nothing running
                server_thread = threading.Thread(
                    target=lambda: asyncio.run(_go()))
                server_thread.start()
                self._server_running = True
            else:
                logger.warning(
                    f'Proxy server connection test to {host}:{port} '
                    f'returned status {status}')

    def send(self, user_id: int, client_id: str, data: dict) -> bool:
        """
        Send dictionary data to a client associated with the specified user.

        :param user_id: ID of the user whose client to send data to
        :param client_id: ID of the client belonging to the user to send data to
        :param data: the data to send
        :return: ``True`` if sending was successful; ``False`` otherwise
        """
        if not self._server_running:
            logger.error('Proxy server is not running')
            return False

        if not clients.contains(user_id, client_id):
            logger.error(f'user {user_id} has no associated client with ID '
                         f'{client_id!r}')
            return False

        clients.get(user_id, client_id).protocol.send(data)
        return True


proxy_server = ProxyServer()
