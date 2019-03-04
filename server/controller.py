import os
import subprocess
import asyncio

from pathlib import Path
from definitions import ROOT_DIR


class Controller:
    """
    Controls for lighting configuration.
    """

    def __init__(self, debug=False):
        self.debug = debug
        self._current_proc: subprocess.Popen = None

    def debug_log(self, v):
        if self.debug:
            print(v)

    @staticmethod
    def get_script_names() -> list:
        """
        Get the names of available Fadecandy scripts.

        :return: a list of names of existing scripts
        """
        ignore = ['__pycache__', '__init__.py', 'opc.py', 'opcutil.py']
        return list(map(lambda e: e[:-3],
                        filter(lambda e: e not in ignore,
                               os.listdir(ROOT_DIR + '/server/scripts'))))

    def run_script(self, name: str) -> bool:
        """
        Run the Fadecandy script with the given name. Requires a Fadecandy
        server to be started.

        :param name: the name of the script to run
        :return: True if script exists, False otherwise
        """
        async def _go(_path: str) -> subprocess.Popen:
            return subprocess.Popen(['python', _path])

        path = f'{ROOT_DIR}/server/scripts/{name}.py'
        script = Path(path)
        if script.is_file():
            if self._current_proc:
                self.debug_log(f'Terminating {self._current_proc}')
                self._current_proc.terminate()

            self.debug_log(f'Running {name}.py')
            self._current_proc = asyncio.run(_go(path))
            return True
        else:
            return False
