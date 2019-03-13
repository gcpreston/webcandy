import os
import subprocess
import asyncio
import re
import logging
import json

from pathlib import Path
from definitions import ROOT_DIR


class Controller:
    """
    Controls for lighting configuration.
    """

    def __init__(self, debug=False):
        self.debug = debug
        self._current_proc: subprocess.Popen = None

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

    @staticmethod
    def get_saved_colors() -> dict:
        """
        Retrieve the contents of the saved_colors.json file.

        :return: a mapping from name to hex value of the saved colors
        """
        with open(ROOT_DIR + '/server/assets/saved_colors.json') as file:
            return json.load(file)

    def run_script(self, name: str, color: str = None) -> bool:
        """
        Run the Fadecandy script with the given name. Requires a Fadecandy
        server to be started.

        :param name: the name of the script to run
        :param color: the hex of the color to display (#RRGGBB); for use in
            solid_color.py
        :return: True if a script was successfully executed, False otherwise
        """

        async def _go(_path: str) -> subprocess.Popen:
            # TODO: Explicit Python path
            args = ['python', _path]
            if color:
                args.append(color)
            return subprocess.Popen(args)

        path = f'{ROOT_DIR}/server/scripts/{name}.py'
        script = Path(path)
        if script.is_file():
            # terminate script currently running
            if self._current_proc:
                logging.debug(f'Terminating {self._current_proc}')
                self._current_proc.terminate()

            if name == 'color' and not re.match(r'^#[A-Fa-f0-9]{6}$', color):
                logging.warning('Invalid color provided. '
                                'No script will be run. ')
            else:
                logging.debug(f'Running {name}.py')
                self._current_proc = asyncio.run(_go(path))
                return False

            return True
        else:
            return False
