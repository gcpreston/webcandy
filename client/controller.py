import multiprocessing
import logging

from opclib.interface import LightConfig


def _execute(**kwargs) -> None:
    """
    Run the specified lighting configuration.

    :param kwargs: keyword arguments to pass to ``LightConfig`` factory
    :raises ValueError: if the specified configuration was not given properly
        formatted data
    """
    LightConfig.factory(**kwargs).run()


class Controller:
    """
    Controls for lighting configuration.
    """

    _current_proc: multiprocessing.Process = None

    def run_config(self, **kwargs) -> None:
        """
        Run the Fadecandy script with the given name. Requires a Fadecandy
        server to be started.

        :param kwargs: arguments to pass to the specified light config
        """
        if self._current_proc and self._current_proc.is_alive():
            logging.debug(f'Terminating {self._current_proc}')
            self._current_proc.terminate()

        logging.info(f'Attempting to run configuration: {kwargs}')
        self._current_proc = multiprocessing.Process(target=_execute,
                                                     kwargs=kwargs)
        self._current_proc.start()