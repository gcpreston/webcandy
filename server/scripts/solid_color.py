import sys
import time
import re
import logging

from . import opc


def get_color(hex):
    """
    Calculate a 3-tuple representing the color in the given hex.

    :param hex: the desired color in the format #RRGGBB.
    """
    red = int(hex[1:3], 16)
    blue = int(hex[3:5], 16)
    green = int(hex[5:7], 16)

    return tuple([red, blue, green])


def run(color=None, *args, **kwargs):
    if not color or not re.match(r'^#[A-Fa-f0-9]{6}$', color):
        raise ValueError(f'Please provide a color in the format #RRGGBB. Received {color}.')

    num_leds = 512
    client = opc.Client('localhost:7890')

    black = [(0, 0, 0)] * num_leds
    color = [get_color(color)] * num_leds

    client.put_pixels(black)
    client.put_pixels(black)
    time.sleep(0.5)
    client.put_pixels(color)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Please provide a color in the format #RRGGBB.')
    
    run(color=sys.argv[-1])
