import abc
import re

from . import opc


class LightConfig(abc.ABC):
    """
    Abstract base class for an LED lighting configuration.
    """

    def __init__(self, port: int = 7890, num_leds: int = 512):
        """
        Initialize a new LightConfig.

        :param port: the port the Fadecandy server is running on
        :param num_leds: the number of LEDs
        """
        self.client: opc.Client = opc.Client(f'localhost:{port}')
        self.num_leds: int = num_leds

    @staticmethod
    def factory(name: str, color: str = None) -> 'LightConfig':
        """
        Create an instance of a specific light configuration based on the given name.

        :param name: the name of the desired lighting configuration
        :param color: the color to display for solid_color
        :return: an instance of the class associated with ``name``
        :raises ValueError: if ``name`` is not associated with any lighting configurations
        """
        if name == 'fade':
            from .fade import Fade
            return Fade()
        elif name == 'strobe':
            from .strobe import Strobe
            return Strobe()
        elif name == 'rainbow_scroll':
            from .rainbow_scroll import RainbowScroll
            return RainbowScroll()
        elif name == 'rainbow_strobe':
            from .rainbow_strobe import RainbowStrobe
            return RainbowStrobe()
        elif name == 'solid_color':
            from .solid_color import SolidColor

            if not color or not re.match(r'^#[A-Fa-f0-9]{6}$', color):
                raise ValueError(
                    f"Please provide a color in the format #RRGGBB. Received '{color}'.")

            return SolidColor(color)
        elif name == 'off':
            from .off import Off
            return Off()

        raise ValueError(f"'{name}' is not associated with any lighting configurations")

    @abc.abstractmethod
    def run(self) -> None:
        """
        Run this lighting configuration.
        """
        pass
