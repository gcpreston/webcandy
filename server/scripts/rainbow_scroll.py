import time

from . import opcutil
from .interface import LightConfig


class RainbowScroll(LightConfig):
    """
    Scroll through a rainbow of colors.
    """

    def run(self, *args, **kwargs):
        colors = [(255, 0, 0),  # red
                  (255, 127, 0),  # orange
                  (255, 255, 0),  # yellow
                  (0, 255, 0),  # green
                  (0, 0, 255),  # blue
                  (139, 0, 255)]  # violet
        pixels = opcutil.spread(colors, self.num_leds, 10)

        while True:
            self.client.put_pixels(pixels)
            time.sleep(0.1)
            pixels = opcutil.rotate_right(pixels, 1)
