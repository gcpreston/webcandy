import sys
import subprocess
import socket
import asyncio
import atexit
import logging

from definitions import ROOT_DIR


class FadecandyServer:
    """
    Controller for Fadecandy server.
    """

    _server_running: bool = False
    _fcserver_proc: subprocess.Popen = None

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
            logging.info(f'Started {server}')
            _fcserver_proc = subprocess.Popen(ROOT_DIR + '/bin/' + server)
            return _fcserver_proc

        if not self._server_running:
            # check if other instance of fcserver is running on port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('127.0.0.1', 7890))

            if result == 10061:  # nothing running
                self._fcserver_proc = asyncio.run(_go())
                self._server_running = True

                atexit.register(self.stop)  # stop fcserver on exit
            else:
                logging.debug('Another instance of fcserver is already running')

    def stop(self) -> None:
        """
        Stop the Fadecandy server.
        """
        self._fcserver_proc.terminate()
        self._server_running = False
        logging.info('Stopped fcserver')
