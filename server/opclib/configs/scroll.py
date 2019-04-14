from typing import List
from ..interface import DynamicLightConfig
from ..opcutil import get_color, spread, rotate_right


class Scroll(DynamicLightConfig):
    """
    Scroll through a multi-colored line.
    """
    speed = 10

    def __init__(self, colors: List[str]):
        """
        Initialize a new Scroll configuration.
        :param colors: the colors to use ("#RRGGBB" format)
        """
        super().__init__()
        self.colors = [get_color(c) for c in colors]
        self.pixels = spread(self.colors, self.num_leds, 10)

    def __next__(self):
        self.pixels = rotate_right(self.pixels, 1)
        return self.pixels
