import socket
import threading
import asyncio
import atexit
import util

from flask import Flask


class WebcandyClientManager:
    """
    Class to manage client socket connections.
    """

    reader: asyncio.StreamReader = None
    writer: asyncio.StreamWriter = None
    _server_running: bool = False

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

        async def _start_server():
            server = await asyncio.start_server(_handle_connection,
                                                self.host, self.port)
            self._server_running = True
            addr = server.sockets[0].getsockname()
            self.app.logger.info(f'Serving on {util.format_addr(addr)}')

            async with server:
                await server.serve_forever()

        def _handle_connection(reader, writer):
            addr = writer.get_extra_info('peername')
            self.app.logger.info(f'Connected client {util.format_addr(addr)}')
            # set reader and writer to most recent connection
            # TODO: Handle multiple connections
            self.reader = reader
            self.writer = writer

        if not self._server_running:
            # test if other instance is already running
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_sock:
                result = test_sock.connect_ex((self.host, self.port))

            if result == 10061:  # nothing running
                # start server loop in separate thread
                server_thread = threading.Thread(
                    target=lambda: asyncio.run(_start_server()))
                server_thread.start()

                atexit.register(self.stop)

    def stop(self) -> None:
        """
        Stop this ``WebcandyClientManager``.
        """
        self.app.logger.info('Stopped client manager server')
        self.writer.close()
        self._server_running = False

    def send(self, data: bytes) -> bool:
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
