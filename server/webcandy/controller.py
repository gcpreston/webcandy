import os
import multiprocessing
import importlib
import re
import json

from definitions import ROOT_DIR
from webcandy import app


def run_script(name: str, color: str):
    """
    Execute the run function on the specified script module.

    :param name: the name of the script to run
    :param color: the color parameter for solid_color
    """
    try:
        script = importlib.import_module(f'scripts.{name}')
        script.run(color)
    except ModuleNotFoundError:
        app.logger.error(f'Script {name} not found.')
    except ValueError as e:
        app.logger.error(e)


class Controller:
    """
    Controls for lighting configuration.
    """

    _current_proc: multiprocessing.Process = None

    @staticmethod
    def get_script_names() -> list:
        """
        Get the names of available Fadecandy scripts.

        :return: a list of names of existing scripts
        """
        ignore = ['__pycache__', '__init__.py', 'opc.py', 'opcutil.py',
                  'solid_color.py', 'off.py']
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
    
    def execute_script(self, name: str, color: str = None):
        """
        Run the Fadecandy script with the given name. Requires a Fadecandy
        server to be started.

        :param name: the name of the script to run
        :param color: the hex of the color to display (#RRGGBB); for use in
            solid_color.py
        """
        if self._current_proc and self._current_proc.is_alive():
            app.logger.debug(f'Terminating {self._current_proc}')
            self._current_proc.terminate()

        app.logger.debug(f'Running {name}')
        self._current_proc = multiprocessing.Process(target=run_script, args=(name, color,))
        self._current_proc.start()
