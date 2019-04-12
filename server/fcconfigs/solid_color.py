import time

from .opcutil import get_color
from .interface import LightConfig


class SolidColor(LightConfig):
    """
    Display a solid color.
    """

    def __init__(self, color: str):
        """
        Initialize a new SolidColor configuration.
        :param color: the color to dislpay (in format "#RRGGBB")
        """
        super().__init__()
        self.color = color

    def run(self):
        black = [(0, 0, 0)] * self.num_leds
        color = [get_color(self.color)] * self.num_leds

        self.client.put_pixels(black)
        self.client.put_pixels(black)
        time.sleep(0.5)
        self.client.put_pixels(color)
