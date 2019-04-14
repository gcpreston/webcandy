from .interface import DynamicLightConfig


# TODO: Abstract the strobe effect
class Strobe(DynamicLightConfig):
    """
    A white, strobing light.
    """
    _on = True

    def __next__(self):
        if self._on:
            return [(0, 0, 0)] * self.num_leds
        else:
            return [(255, 255, 255)] * self.num_leds
