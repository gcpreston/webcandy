from ..interface import LightConfig, DynamicLightConfig
from .solid_color import SolidColor


class Strobe(DynamicLightConfig):
    """
    Add a strobe effect to a given ``LightConfig``.
    """
    speed = 20
    _on = True

    def __init__(self, config: LightConfig = SolidColor('#FFFFFF'),
                 speed: int = None, num_leds: int = 512, port: int = 7890):
        """
        Initialize a new Stobe.

        :param config: the light config to add a strobe effect to
        :param speed: the speed at which the lights change (updates per second)
        :param num_leds: the number of LEDs
        :param port: the port the Fadecandy server is running on
        """
        super().__init__(speed, num_leds, port)
        self._config = config

    def __next__(self):
        # TODO: Separately control animation speed and strobe speed
        self._on = not self._on
        pixels = next(self._config)

        if self._on:
            return [(0, 0, 0)] * self.num_leds
        else:
            return pixels
