import os
import multiprocessing
import json

from scripts.interface import LightConfig
from flask import Flask
from logging import Logger
from definitions import ROOT_DIR


def _execute(logger: Logger, name: str, color: str = None):
    """
    Execute the run function on the specified script module.

    :param logger: the logger to output to
    :param name: the name of the script to run
    :param color: the hex of the color to display (#RRGGBB); for use with solid_color
    """
    try:
        LightConfig.factory(name, color=color).run()
    except ValueError as e:
        # name was not recognized or color is misformatted
        logger.error(e)


class Controller:
    """
    Controls for lighting configuration.
    """

    app: Flask = None
    _current_proc: multiprocessing.Process = None

    def init_app(self, app: Flask):
        """
        Register this Controller with a Flask app.
        """
        self.app = app

    @staticmethod
    def get_script_names() -> list:
        """
        Get the names of available Fadecandy scripts.
        :return: a list of names of existing scripts
        """
        ignore = {'__pycache__', '__init__.py', 'opc.py', 'opcutil.py', 'interface.py',
                  'solid_color.py', 'off.py'}
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

    def run_script(self, name: str, color: str = None) -> None:
        """
        Run the Fadecandy script with the given name. Requires a Fadecandy server to be started.

        :param name: the name of the script to run
        :param color: the hex of the color to display (#RRGGBB); for use in solid_color
        """
        if self._current_proc and self._current_proc.is_alive():
            self.app.logger.debug(f'Terminating {self._current_proc}')
            self._current_proc.terminate()

        self.app.logger.info(f'Running script: {name}, color: {color}')
        self._current_proc = multiprocessing.Process(target=_execute,
                                                     args=(self.app.logger, name, color))
        self._current_proc.start()
