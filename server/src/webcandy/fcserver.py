import sys
import subprocess
import socket
import asyncio
import atexit

from flask import Flask
from types import FunctionType
from definitions import ROOT_DIR


class FCServer:
    """
    Controller for Fadecandy server.
    """

    app: Flask = None
    _server_running: bool = False
    _fcserver_proc: subprocess.Popen = None

    def init_app(self, app: Flask):
        """
        Register this FCServer with a Flask app.
        """
        self.app = app

    def start(self) -> None:
        """
        Run the Fadecandy server. Terminates on program exit.
        """

        async def _go():
            if sys.platform == 'win32':
                server = 'fcserver.exe'
            elif sys.platform == 'darwin':
                server = 'fcserver-osx'
            else:
                server = 'fcserver-rpi'
            _fcserver_proc = subprocess.Popen(ROOT_DIR + '/bin/' + server)
            return _fcserver_proc

        if not self._server_running:
            # check if other instance of fcserver is running on port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('127.0.0.1', 7890))

            if result == 10061:  # nothing running
                self._fcserver_proc = asyncio.run(_go())
                self._server_running = True
                self.app.logger.info('Started fcserver')

                atexit.register(self.stop)  # stop fcserver on exit

    def stop(self) -> None:
        """
        Stop the Fadecandy server.
        """
        self._fcserver_proc.terminate()
        self._server_running = False
        self.app.logger.info('Stopped fcserver')
