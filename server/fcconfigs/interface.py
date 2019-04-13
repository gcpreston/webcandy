import abc
import time

from typing import NewType, List, Tuple
from . import opc
from .opcutil import is_color

Color = NewType('Color', Tuple[float, float, float])

# IDEA
# Lighting configurations are iterators that generate the next list of pixels
# to put onto an LED strip. The run method steps through the iterator and does
# the work of pushing the generated list to the Fadecandy client.


# TODO: Add ability to control brightness
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

    def __iter__(self):
        """
        Define any LightConfig to be iterable.
        :return: self
        """
        return self

    @abc.abstractmethod
    def __next__(self):
        """
        Generate the next list of colors to push to the Fadecandy client.
        :return: the new colors
        """
        pass

    @staticmethod
    def factory(name: str, **kwargs) -> 'LightConfig':
        """
        Create an instance of a specific light configuration based on the given
        name.

        :param name: the name of the desired lighting configuration
        :return: an instance of the class associated with ``name``
        :raises ValueError: if ``name`` is not associated with any configs
        """

        def get_color():
            """
            Extract the color field from ``kwargs``.
            :return: the color string (#RRGGBB)
            :raises ValueError: if a color of the correct format is not found
            """
            color = kwargs.get('color')
            if not color or not is_color(color):
                color_repr = f"'{color}'" if color else None
                raise ValueError(
                    "Please provide a color in the format #RRGGBB. "
                    f"Received {color_repr}.")
            return color

        def get_colors():
            """
            Extract the colors field from ``kwargs``.
            :return: the list of color strings (#RRGGBB)
            :raises ValueError: if a list of correctly formatted colors is not
                found
            """
            colors = kwargs.get('colors')
            if not colors or not all([is_color(c) for c in colors]):
                raise ValueError(
                    "Please provide a list of colors in the format #RRGGBB. "
                    f"Received {colors}.")
            return colors

        def set_speed(light_config: LightConfig) -> LightConfig:
            """
            Set the speed of the given ``LightConfig`` to the value specified
            in ``kwargs``, if one is found.
            :param light_config: the ``LightConfig`` to set the speed of
            :return: ``light_config`` updated
            """
            speed = kwargs.get('speed')
            if speed:
                light_config.speed = speed
            return light_config

        if name == 'fade':
            from .fade import Fade
            return set_speed(Fade(get_colors()))
        elif name == 'strobe':
            from .strobe import Strobe
            return set_speed(Strobe())
        elif name == 'scroll':
            from .scroll import Scroll
            return set_speed(Scroll(get_colors()))
        elif name == 'scroll_strobe':
            from .scroll_strobe import ScrollStrobe
            return set_speed(ScrollStrobe(get_colors()))
        elif name == 'solid_color':
            from .solid_color import SolidColor
            return SolidColor(get_color())
        elif name == 'off':
            from .off import Off
            return Off()
        else:
            raise ValueError(
                f"'{name}' is not associated with any lighting configurations")

    @abc.abstractmethod
    def run(self) -> None:
        """
        Run this lighting configuration.
        """
        # TODO: Fade in?
        pass


class StaticLightConfig(LightConfig, abc.ABC):
    """
    A lighting configuration that displays an unmoving pattern.
    """

    def __next__(self):
        return self.pattern()

    def run(self) -> None:
        self.client.put_pixels(self.pattern())

    @abc.abstractmethod
    def pattern(self) -> List[Color]:
        """
        Define the pattern this lighting configuration should display.
        :return: a list of RGB values to display
        """
        pass


class DynamicLightConfig(LightConfig, abc.ABC):
    """
    A lighting configuration that displays a moving pattern.
    """

    def __init__(self, port: int = 7890, num_leds: int = 512, speed: int = 10):
        """
        Initialize a new LightConfig.

        :param port: the port the Fadecandy server is running on
        :param num_leds: the number of LEDs
        :param speed: the speed at which the lights change (updates per second)
        """
        super().__init__(port, num_leds)
        self.speed = speed

    def run(self) -> None:
        while True:
            pixels = next(self)
            print(pixels)
            self.client.put_pixels(pixels)
            time.sleep(1 / self.speed)
