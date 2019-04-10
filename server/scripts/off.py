import time

from .interface import LightConfig


class Off(LightConfig):
    """
    Turn the LEDs off.
    """

    def run(self):
        black = [(0, 0, 0)] * self.num_leds

        self.client.put_pixels(black)
        self.client.put_pixels(black)
        time.sleep(0.5)
        self.client.put_pixels(black)
