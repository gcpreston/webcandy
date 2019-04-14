from typing import Tuple
from ..interface import StaticLightConfig
from ..opcutil import get_color


class SolidColor(StaticLightConfig):
    """
    Display a solid color.
    """

    def __init__(self, color: str):
        """
        Initialize a new SolidColor configuration.
        :param color: the color to dislpay (in format "#RRGGBB")
        """
        super().__init__()
        self.color: Tuple[int, int, int] = get_color(color)

    def pattern(self):
        return [self.color] * self.num_leds
