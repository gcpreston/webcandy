import time

from typing import List
from ..interface import LightConfig
from ..opcutil import get_color, spread, rotate_right


class ScrollStrobe(LightConfig):
    """
    A Scroll configuration that also strobes.
    """

    def __init__(self, colors: List[str]):
        """
        Initialize a new ScrollStrobe configuration.
        :param colors: the colors to use ("#RRGGBB" format)
        """
        super().__init__()
        self.colors = [get_color(c) for c in colors]

    def run(self):
        pixels = spread(self.colors, self.num_leds, 10)
        black = [(0, 0, 0)] * self.num_leds

        while True:
            self.client.put_pixels(pixels)
            time.sleep(0.05)
            pixels = rotate_right(pixels, 2)
            self.client.put_pixels(black)
            time.sleep(0.05)
