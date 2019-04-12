import time

from typing import List
from .interface import LightConfig
from .opcutil import get_color, shift


class Fade(LightConfig):
    """
    Fade between specified colors.
    """

    def __init__(self, colors: List[str]):
        """
        Initialize a new Fade configuration.
        :param colors: the colors to use ("#RRGGBB" format)
        """
        super().__init__()
        self.colors = [get_color(c) for c in colors]

    def run(self):
        i = 0
        current = self.colors[i]
        pixels = [current] * self.num_leds

        while True:
            i = (i + 1) % len(self.colors)
            for _ in range(10):
                self.client.put_pixels(pixels)
                current = shift(current, self.colors[i], 0.1)
                pixels = [current] * self.num_leds
                time.sleep(0.5)
