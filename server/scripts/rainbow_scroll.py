import time

from typing import List
from .opcutil import get_color, spread, rotate_right
from .interface import LightConfig


class RainbowScroll(LightConfig):
    """
    Scroll through a rainbow of colors.
    """

    def __init__(self, colors: List[str]):
        """
        Initialize a new Fade configuration
        :param colors: the list of colors to use in the scroll (#RRGGBB format)
        """
        super().__init__()
        self.colors = [get_color(c) for c in colors]

    def run(self, *args, **kwargs):
        pixels = spread(self.colors, self.num_leds, 10)

        while True:
            self.client.put_pixels(pixels)
            time.sleep(0.1)
            pixels = rotate_right(pixels, 1)
