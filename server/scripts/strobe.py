import time

from .interface import LightConfig


class Strobe(LightConfig):
    """
    A white, strobing light.
    """

    def run(self):
        black = [(0, 0, 0)] * self.num_leds
        white = [(255, 255, 255)] * self.num_leds

        while True:
            self.client.put_pixels(white)
            time.sleep(0.05)
            self.client.put_pixels(black)
            time.sleep(0.05)
