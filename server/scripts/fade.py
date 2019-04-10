import time

from typing import List
from . import opcutil
from .interface import LightConfig


class Fade(LightConfig):
    """
    Fade between specified colors.
    """

    def __init__(self, colors: List[str]):
        """
        Initialize a new Fade configuration
        :param colors: the colors to fade between
        """
        super().__init__()
        self.colors = colors

    def run(self):
        colors = [(255, 0, 0),    # red
                  (255, 127, 0),  # orange
                  (255, 255, 0),  # yellow
                  (0, 255, 0),    # green
                  (0, 0, 255),    # blue
                  (139, 0, 255)]  # violet
        i = 0
        current = colors[i]
        pixels = [current] * self.num_leds

        while True:
            i = (i + 1) % len(colors)
            for _ in range(10):
                self.client.put_pixels(pixels)
                current = opcutil.shift(current, colors[i], 0.1)
                pixels = [current] * self.num_leds
                time.sleep(0.5)
