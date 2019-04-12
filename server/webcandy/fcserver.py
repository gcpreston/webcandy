import sys
import subprocess
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

        async def _go(stop_fn: FunctionType):
            if sys.platform == 'win32':
                server = 'fcserver.exe'
            elif sys.platform == 'darwin':
                server = 'fcserver-osx'
            else:
                server = 'fcserver-rpi'
            _fcserver_proc = subprocess.Popen(ROOT_DIR + '/bin/' + server)
            atexit.register(stop_fn)
            return _fcserver_proc

        if not self._server_running:
            self._fcserver_proc = asyncio.run(_go(self.stop))
            self._server_running = True
            self.app.logger.info('Started fcserver')

    def stop(self) -> None:
        """
        Stop the Fadecandy server.
        """
        self._fcserver_proc.terminate()
        self._server_running = False
        self.app.logger.info('Stopped fcserver')
