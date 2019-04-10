import time

from .opcutil import spread, rotate_right
from .interface import LightConfig


class RainbowScroll(LightConfig):
    """
    Scroll through a rainbow of colors.
    """

    def run(self, *args, **kwargs):
        # TODO: Abstract colors
        colors = [(255, 0, 0),    # red
                  (255, 127, 0),  # orange
                  (255, 255, 0),  # yellow
                  (0, 255, 0),    # green
                  (0, 0, 255),    # blue
                  (139, 0, 255)]  # violet
        pixels = spread(colors, self.num_leds, 10)

        while True:
            self.client.put_pixels(pixels)
            time.sleep(0.1)
            pixels = rotate_right(pixels, 1)
