from typing import List
from ..interface import DynamicLightConfig
from ..opcutil import get_color, shift


class Fade(DynamicLightConfig):
    """
    Fade between specified colors.
    """
    _color_index = 0  # index of color being faded towards in self.colors
    _fade_index = 0  # how far we are between two colors [0-9]
    speed = 5

    def __init__(self, colors: List[str], speed: int = None,
                 num_leds: int = 512, port: int = 7890):
        """
        Initialize a new Fade configuration.
        :param colors: the colors to use ("#RRGGBB" format)
        """
        super().__init__(speed, num_leds, port)
        self.colors = [get_color(c) for c in colors]
        self._current_color = self.colors[0]
        self.pixels = [self._current_color] * self.num_leds

    def __next__(self):
        if self._fade_index == 9:
            # go to next color
            self._color_index = (self._color_index + 1) % len(self.colors)

        # increment _fade_index, or wrap back to 0
        self._fade_index = (self._fade_index + 1) % 10

        # shift pixels 10% towards the next color
        self._current_color = shift(self._current_color,
                                    self.colors[self._color_index], 0.1)
        self.pixels = [self._current_color] * self.num_leds

        return self.pixels
