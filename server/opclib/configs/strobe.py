from ..interface import DynamicLightConfig


# TODO: Abstract the strobe effect
class Strobe(DynamicLightConfig):
    """
    A white, strobing light.
    """
    speed = 20
    _on = True

    def __next__(self):
        self._on = not self._on
        if self._on:
            return [(0, 0, 0)] * self.num_leds
        else:
            return [(255, 255, 255)] * self.num_leds
