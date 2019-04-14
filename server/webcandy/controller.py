import multiprocessing
import util

from opclib.interface import LightConfig
from flask import Flask


def _execute(name: str, **kwargs) -> None:
    """
    Run the specified lighting configuration.

    :param name: the name of the configuration to run
    :param kwargs: keyword arguments to pass to ``LightConfig`` factory
    :raises ValueError: if the specified configuration was not given properly
        formatted data
    """
    LightConfig.factory(name, **kwargs).run()


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

    def run_script(self, name: str, color: str = None) -> None:
        """
        Run the Fadecandy script with the given name. Requires a Fadecandy
        server to be started.

        :param name: the name of the script to run
        :param color: the hex of the color to display (#RRGGBB); for use in
            solid_color
        """
        if self._current_proc and self._current_proc.is_alive():
            self.app.logger.debug(f'Terminating {self._current_proc}')
            self._current_proc.terminate()

        # TODO: Allow colors to be configurable
        # initialize default colors
        colors = util.load_asset('color_lists.json')['default']
        kwargs = {'color': color, 'colors': colors}

        self.app.logger.info(f'Running script: {name}, color: {color}')
        self._current_proc = multiprocessing.Process(target=_execute,
                                                     args=(name,),
                                                     kwargs=kwargs)
        self._current_proc.start()
