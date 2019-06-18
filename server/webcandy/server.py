import asyncio
import socket
import threading
import json
import logging
import websockets

from collections import defaultdict
from typing import NewType, Tuple, List, Dict
from flask import Flask
from websockets.server import WebSocketServerProtocol

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
                             f' from {util.format_addr(protocol.remote_address)}')
                protocol.send('Invalid authentication token.\n')
                protocol.close()

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

        self.clients[user_id][client_id].protocol.close()
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


class WebcandyServerProtocol(WebSocketServerProtocol):
    # these must be set
    user_id: int
    client_id: str

    def init(self, user_id: int, client_id: str) -> None:
        """
        Set required fields for this protocol.

        :param user_id: the user owning the client this protocol represents
        :param client_id: the ID of the client this protocol represents
        """
        self.user_id = user_id
        self.client_id = client_id

    def connection_made(self, transport):
        super().connection_made(transport)
        logger.info(f'Connected client {self.remote_address}')

    def connection_lost(self, exc):
        super().connection_lost(exc)
        logger.info(f'Disconnected user {self.user_id}, '
                    f'client {self.client_id!r} '
                    f'({util.format_addr(self.remote_address)})')


class ProxyServer:
    """
    Manager for the proxy server allowing data to be sent to specific clients.
    """
    running: bool = False

    @staticmethod
    async def _handler(client, _):
        addr = util.format_addr(client.remote_address)

        data = await client.recv()
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            logger.info(f'Received text from {addr}: {data!r}')
            return

        token = parsed.get('token')
        client_id = parsed.get('client_id')
        patterns = parsed.get('patterns')

        if token is None:
            logger.error(f'Missing token in data from {addr}')
            client.send("[ERROR] Please provide an authentication "
                        "token in a 'token' field.\n")
            client.close()
            return
        if client_id is None:
            logger.error(f'Missing client_id in data from {addr}')
            client.send("[ERROR] Please provide a client ID in a "
                        "'client_id' field.\n")
            client.close()
            return
        if patterns is None:
            logger.error(f'Missing patterns in data from {addr}')
            client.send("[ERROR] Please provide the client's "
                        "available patterns in a 'patterns' field.\n")
            client.close()
            return

        clients.register(token, client_id, patterns, client)

    def start(self, host: str = '127.0.0.1', port: int = 6543) -> None:
        """
        Start the proxy server.

        :param host: the host to serve on
        :param port: the port to serve on
        """

        def _go(handler):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            start_server = websockets.serve(
                handler, host, port, create_protocol=WebcandyServerProtocol)

            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()

        if not self.running:
            # test if other instance is already running
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
                status = test_sock.connect_ex((host, port))

        # check for both Windows and Linux status codes
        if status in {10061, 111}:  # nothing running
            server_thread = threading.Thread(
                target=_go, args=(ProxyServer._handler,))
            server_thread.start()
            self.running = True
            logger.info(f'Proxy server bound to {host}:{port}')
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
        if not self.running:
            logger.error('Proxy server is not running')
            return False

        if not clients.contains(user_id, client_id):
            logger.error(f'user {user_id} has no associated client with ID '
                         f'{client_id!r}')
            return False

        clients.get(user_id, client_id).protocol.send(data)
        return True


proxy_server = ProxyServer()
