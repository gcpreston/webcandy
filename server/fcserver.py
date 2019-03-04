# import sys
import subprocess
import asyncio
import atexit

from types import FunctionType
from definitions import ROOT_DIR


class FCServer:
    """
    Controller for Fadecandy server.
    """

    def __init__(self):
        # TODO: Switch over sys.platform
        self._server_running: bool = False
        self._fcserver_proc: subprocess.Popen = None

    def start(self) -> None:
        """
        Run the Fadecandy server. Terminates on program exit.
        """
        async def _go(stop_fn: FunctionType):
            _fcserver_proc = subprocess.Popen(ROOT_DIR + '/bin/fcserver.exe')
            atexit.register(stop_fn)
            return _fcserver_proc

        if not self._server_running:
            self._server_running = True
            self._fcserver_proc = asyncio.run(_go(self.stop))

    def stop(self) -> None:
        """
        Stop the Fadecandy serer.
        """
        print('Stopping fcserver...')
        self._server_running = False
        self._fcserver_proc.terminate()
