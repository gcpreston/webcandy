from typing import List
from opclib.interface import Color
from .. import opcutil
from ..interface import StaticLightConfig


class Stripes(StaticLightConfig):
    """
    Display multiple static colors.
    """

    def __init__(self, colors: List[str], num_leds: int = 512,
                 port: int = 7890):
        super().__init__(num_leds, port)
        self.colors = [opcutil.get_color(c) for c in colors]

    def pattern(self) -> List[Color]:
        return opcutil.spread(self.colors, self.num_leds, 10)
