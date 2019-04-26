import socket
import threading
import asyncio
import util

from flask import Flask


class WebcandyClientManager:
    """
    Class to manage client socket connections.
    """

    reader: asyncio.StreamReader = None
    writer: asyncio.StreamWriter = None

    def __init__(self, app: Flask = None, host: str = '127.0.0.1',
                 port: int = 6543):
        self.app = app
        self.host = host
        self.port = port

    def init_app(self, app):
        self.app = app

    def start(self) -> None:
        """
        Start this ``WebcandyClientManager``.
        """

        async def _init_server():
            server = await asyncio.start_server(_handle_connection, self.host, self.port)
            addr = server.sockets[0].getsockname()
            self.app.logger.info(f'Serving on {util.format_addr(addr)}')

            async with server:
                await server.serve_forever()

        def _handle_connection(reader, writer):
            addr = writer.get_extra_info('peername')
            self.app.logger.info(f'Connected client {util.format_addr(addr)}')
            # set reader and writer to most recent connection
            self.reader = reader
            self.writer = writer

        def _run_server():
            # test if manager is already running
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
                result = test_sock.connect_ex((self.host, self.port))

            if result == 10061:  # nothing running
                asyncio.run(_init_server())

        # start server loop in separate thread
        server_thread = threading.Thread(target=_run_server)
        server_thread.start()

    def send(self, data) -> bool:
        """
        Send data to a client.
        :param data: the data to send
        :return: ``True`` if the operation was successful; ``False`` otherwise
        """
        try:
            self.writer.write(data)
        except AttributeError:
            self.app.logger.error('No client connection established')
            return False
        except OSError as e:
            self.app.logger.error(e)
            return False
        return True
