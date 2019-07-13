import asyncio
import socket
import threading
import json
import logging
import websockets

from collections import defaultdict
from typing import Dict, List
from flask import Flask

from . import util
from .config import configure_logger
from .models import User

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

        def __init__(self, user_id: int, client_id: str, patterns: List[str],
                     protocol: 'WebcandyServerProtocol'):
            # store user_id and client_id as backward reference
            self.user_id = user_id
            self.client_id = client_id
            self.patterns = patterns
            self.protocol = protocol

    # map user_id to map of client_id to Client instance
    clients: Dict[int, Dict[str, Client]] = defaultdict(dict)

    def __init__(self, app: Flask = None):
        self.app = app

    def init_app(self, app: Flask) -> None:
        self.app = app

    def register(self, token: str, client_id: str, patterns: List[str],
                 protocol: 'WebcandyServerProtocol') -> int:
        """
        Register a new client.

        :param token: authorization token provided by the client
        :param client_id: the client ID to use; must be unique for this user
        :param patterns: available patterns provided by the client
        :param protocol: ``WebcandyServerProtocol`` instance for the client
        :return: the user_id the token is associated with
        :raises RuntimeError: if called before app is initialized
        """
        if not self.app:
            raise RuntimeError('app must be initialized to register client')

        with self.app.app_context():
            user: User = User.get_user(token)
            if user:
                self.clients[user.user_id][client_id] = self.Client(
                    user.user_id, client_id, patterns, protocol)
                logger.info(
                    f'Registered client {client_id!r} with user {user.user_id} '
                    f'({util.format_addr(protocol.remote_address)})')
                return user.user_id
            else:
                logger.error(
                    f'No user could be associated with token {token!r}'
                    f'from {util.format_addr(protocol.remote_address)}')
                protocol.send('Invalid authentication token.\n')
                protocol.close()

    def unregister(self, user_id: int, client_id: str) -> None:
        """
        Close a client's transport and unregister it from the client manager.

        :param user_id: the user who owns the client
        :param client_id: the ID of the client to unregister
        :raises ValueError: if user has no associated clients
        """
        if not self.contains(user_id, client_id):
            raise ValueError(f'User {user_id} has no associated client with ID '
                             f'{client_id!r}')

        remote_addr = self.clients[user_id][client_id].protocol.remote_address
        self.clients[user_id][client_id].protocol.close()
        del self.clients[user_id][client_id]
        logger.info(f'Unregistered client {client_id!r} of user {user_id} '
                    f'({util.format_addr(remote_addr)})')

    def available_clients(self, user_id: int) -> List[str]:
        """
        Get a list of IDs of currently connected clients.
        """
        return list(self.clients[user_id])

    def get_client(self, user_id: int, client_id: str) -> Client:
        """
        Get a currently registered client.
        """
        return self.clients[user_id][client_id]

    def contains(self, user_id: int, client_id: str) -> bool:
        """
        Check if a user has a client with the specified ID.
        """
        return client_id in self.clients[user_id]


clients = ClientManager()  # make sure to call init_app on this


class WebcandyServerProtocol(websockets.WebSocketServerProtocol):
    """
    Subclass of WebSocketProtocol for logging purposes. I prefer to use this
    over `websockets` logging because minimal logging messages are needed.
    """

    def connection_made(self, transport):
        super().connection_made(transport)
        logger.debug(
            f'Connected client {util.format_addr(self.remote_address)}')

    def connection_lost(self, exc):
        super().connection_lost(exc)
        logger.debug(
            f'Disconnected client {util.format_addr(self.remote_address)}')


class ProxyServer:
    """
    Manager for the proxy server allowing data to be sent to specific clients.
    """
    running: bool = False

    @staticmethod
    async def _ws_handler(client: WebcandyServerProtocol, _):
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

        user_id = clients.register(token, client_id, patterns, client)

        try:
            await client.wait_closed()
        finally:
            clients.unregister(user_id, client_id)

    # TODO: Get WebSocket server running on the same port as the Flask server,
    #   so the only difference in connecting is the protocol (http:// vs. ws://)
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
                target=_go, args=(ProxyServer._ws_handler,))
            server_thread.start()

            logger.info(f'Proxy server running on ws://{host}:{port}/')
            self.running = True
        else:
            logger.warning(
                f'Connection test to {host}:{port} returned status {status}, '
                'proxy server not started')

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

        asyncio.run(
            clients.get_client(user_id, client_id).protocol.send(
                json.dumps(data)))
        return True


proxy_server = ProxyServer()
