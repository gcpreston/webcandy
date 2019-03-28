import time

from . import opc
from . import opcutil

def run(*args, **kwargs):
    client = opc.Client('localhost:7890')

    num_leds = 512
    colors = [(255, 0, 0),  # red
            (255, 127, 0),  # orange
            (255, 255, 0),  # yellow
            (0, 255, 0),  # green
            (0, 0, 255),  # blue
            (139, 0, 255)]  # violet
    i = 0
    current = colors[i]
    pixels = [current] * num_leds

    while True:
        i = (i + 1) % len(colors)
        for _ in range(10):
            client.put_pixels(pixels)
            current = opcutil.shift(current, colors[i], 0.1)
            pixels = [current] * num_leds
            time.sleep(0.5)


if __name__ == '__main__':
    run()
