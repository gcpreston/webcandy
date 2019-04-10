import time

from . import opcutil
from .interface import LightConfig


class RainbowStrobe(LightConfig):
    """
    Strobe a rainbow of colors.
    """

    def run(self):
        colors = [(255, 0, 0),  # red
                  (255, 127, 0),  # orange
                  (255, 255, 0),  # yellow
                  (0, 255, 0),  # green
                  (0, 0, 255),  # blue
                  (139, 0, 255)]  # violet
        pixels = opcutil.spread(colors, self.num_leds, 10)
        black = [(0, 0, 0)] * self.num_leds

        while True:
            self.client.put_pixels(pixels)
            time.sleep(0.05)
            pixels = opcutil.rotate_right(pixels, 2)
            self.client.put_pixels(black)
            time.sleep(0.05)
