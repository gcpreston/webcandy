import os
import json
import multiprocessing

from scripts.interface import LightConfig
from definitions import ROOT_DIR
from flask import Flask
from logging import Logger
from typing import List, Dict


def _execute(logger: Logger, name: str, color: str = None, colors: List[str] = None):
    """
    Execute the run function on the specified script module.

    :param logger: the logger to output to
    :param name: the name of the script to run
    :param color: the hex of the color to display (#RRGGBB); for use with solid_color
    :param colors: a list of color hexes to display (#RRGGBB); for use with fade
    """
    try:
        LightConfig.factory(name, color=color, colors=colors).run()
    except ValueError as e:
        # name was not recognized or color is misformatted
        logger.error(e)  # TODO: Doesn't format log properly?


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
    def get_script_names() -> List[str]:
        """
        Get the names of available Fadecandy scripts.
        :return: a list of names of existing scripts
        """
        ignore = {'__pycache__', '__init__.py', 'opc.py', 'opcutil.py', 'interface.py',
                  'solid_color.py', 'off.py'}
        return list(map(lambda e: e[:-3],
                        filter(lambda e: e not in ignore,
                               os.listdir(ROOT_DIR + '/server/scripts'))))

    # TODO: saved_solid_colors.json -> saved_colors.json, be able to reference colors by name in
    #   other JSON files
    @staticmethod
    def load_asset(fn: str) -> Dict:
        """
        Retrieve the contents of a specified JSON file in the assets folder

        :param fn: the name of the file to load
        :return: the JSON contents as a dictionary
        """
        with open(f'{ROOT_DIR}/server/assets/{fn}') as file:
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

        # TODO: Allow colors to be configurable
        # initialize default colors
        colors = self.load_asset('saved_fade.json')['default'] if name == 'fade' else []

        self.app.logger.info(f'Running script: {name}, color: {color}')
        self._current_proc = multiprocessing.Process(target=_execute,
                                                     args=(self.app.logger, name, color, colors))
        self._current_proc.start()
