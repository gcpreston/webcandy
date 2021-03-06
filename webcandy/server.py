import asyncio
import socket
import threading
import json
import logging
import websockets

from collections import defaultdict
from typing import Dict, List, Optional
from flask import Flask
from marshmallow import Schema, fields, INCLUDE, ValidationError

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

        def __init__(self, user_id: int, client_name: str, patterns: List[Dict],
                     protocol: websockets.WebSocketServerProtocol):
            # store user_id and client_name as backward reference
            self.user_id = user_id
            self.client_name = client_name
            self.patterns = patterns
            self.protocol = protocol

    # map user_id to map of client_name to Client instance
    clients: Dict[int, Dict[str, Client]] = defaultdict(dict)

    def __init__(self, app: Flask = None):
        self.app = app

    def init_app(self, app: Flask) -> None:
        self.app = app

    def register(self, token: str, client_name: str, patterns: List[Dict],
                 protocol: websockets.WebSocketServerProtocol) \
            -> Optional[User]:
        """
        Register a new client. This method is async in order to be able to send
        messages to `protocol`.
        :param token: authorization token provided by the client
        :param client_name: the client name to use; must be unique for this user
        :param patterns: available patterns provided by the client
        :param protocol: ``WebcandyServerProtocol`` instance for the client
        :return: the user the token is associated with; None if invalid
        :raises RuntimeError: if called before app is initialized
        """
        if not self.app:
            raise RuntimeError('app must be initialized to register client')

        with self.app.app_context():
            user: User = User.get_user(token)
            if user:
                self.clients[user.user_id][client_name] = self.Client(
                    user.user_id, client_name, patterns, protocol)
                logger.info(
                    f'Registered client {client_name!r} '
                    f'with user {user.username!r} '
                    f'({util.format_addr(protocol.remote_address)})')
                return user
            else:
                logger.error(
                    f'No user could be associated with token {token!r}'
                    f'from {util.format_addr(protocol.remote_address)}')
                protocol.close()

    def unregister(self, user_id: int, client_name: str) -> None:
        """
        Close a client's transport and unregister it from the client manager.
        :param user_id: the user who owns the client
        :param client_name: the name of the client to unregister
        :raises ValueError: if user has no associated clients
        """
        with self.app.app_context():
            user: User = User.query.get(user_id)

        if not self.contains(user_id, client_name):
            raise ValueError(f'User {user.username!r} has no associated client '
                             f'named {client_name!r}')

        remote_addr = self.clients[user_id][client_name].protocol.remote_address
        self.clients[user_id][client_name].protocol.close()
        del self.clients[user_id][client_name]
        logger.info(f'Unregistered client {client_name!r} of user '
                    f'{user.username!r} ({util.format_addr(remote_addr)})')

    def available_clients(self, user_id: int) -> List[str]:
        """
        Get a list of names of currently connected clients.
        """
        return list(self.clients[user_id])

    def get_client(self, user_id: int, client_name: str) -> Client:
        """
        Get a currently registered client.
        """
        return self.clients[user_id][client_name]

    def contains(self, user_id: int, client_name: str) -> bool:
        """
        Check if a user has a client with the specified name.
        """
        return client_name in self.clients[user_id]


clients = ClientManager()  # make sure to call init_app on this


class ClientDataSchema(Schema):
    """
    Schema for data that a client must send to get registered.
    """

    class PatternSchema(Schema):
        """
        Schema for necessary information about a lighting pattern.
        """

        class Meta:
            unknown = INCLUDE

        def one_of(*args):
            return lambda v: v in set(args)

        name = fields.Str(required=True)
        type = fields.Str(required=True,
                          validate=one_of('static', 'dynamic'))
        args = fields.List(fields.Str(), required=True)
        default_speed = fields.Float(validate=lambda v: v >= 0)

    token = fields.Str(required=True)
    client_name = fields.Str(required=True)
    patterns = fields.List(fields.Nested(PatternSchema()), required=True)


class ProxyServer:
    """
    Manager for the proxy server allowing data to be sent to specific clients.
    """
    running: bool = False

    @staticmethod
    async def _ws_handler(client: websockets.WebSocketServerProtocol, _):
        addr = util.format_addr(client.remote_address)
        logger.debug(f'Connected client {addr}')

        schema = ClientDataSchema()
        await client.send(
            '[Webcandy] To register a client, please send serialized JSON data '
            'fitting the schema described in the documentation.')

        # loop until schema has been loaded without  errors
        result = None
        while not result:
            data = await client.recv()

            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                logger.debug(
                    f'Data from {addr} could not be decoded to JSON: {data!r}')
                continue

            try:
                result = schema.load(parsed)
            except ValidationError as err:
                logger.error(f'{err.messages} (from {addr})')
                await client.send(f'[Error] {err.messages}')
                continue

        token = result['token']
        client_name = result['client_name']
        patterns = result['patterns']

        user = clients.register(token, client_name, patterns, client)
        if user:
            await clients.get_client(user.user_id, client_name).protocol.send(
                f'Registered client {client_name!r} '
                f'with user {user.username!r}.')
        else:
            await clients.get_client(user.user_id, client_name).protocol.send(
                '[Error] Invalid authentication token\n')

        try:
            await client.wait_closed()
            logger.debug(f'Disconnected client {addr}')
        finally:
            clients.unregister(user.user_id, client_name)

    def start(self, host: str = '127.0.0.1', port: int = 6543) -> None:
        """
        Start the proxy server.
        :param host: the host to serve on
        :param port: the port to serve on
        """

        def _go(handler):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            start_server = websockets.serve(handler, host, port)

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

    def send(self, user_id: int, client_name: str, data: dict) -> bool:
        """
        Send dictionary data to a client associated with the specified user.
        :param user_id: ID of the user whose client to send data to
        :param client_name: name of client to send to
        :param data: the data to send
        :return: ``True`` if sending was successful; ``False`` otherwise
        """
        if not self.running:
            logger.error('Proxy server is not running')
            return False

        if not clients.contains(user_id, client_name):
            logger.error(f'user {user_id} has no associated client named '
                         f'{client_name!r}')
            return False

        asyncio.run(
            clients.get_client(user_id, client_name).protocol.send(
                json.dumps(data)))
        return True


proxy_server = ProxyServer()