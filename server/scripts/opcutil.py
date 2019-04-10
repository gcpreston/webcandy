import re
import time
import math

from typing import Tuple


def is_color(s: str) -> bool:
    """
    Determine if ``s`` is a color hex in the format #RRGGBB.

    :param s: the string to check
    :return: ``True`` if ``s`` fits the pattern; ``False`` otherwise
    """
    return bool(re.match(r'^#[A-Fa-f0-9]{6}$', s))


def get_color(hex_str: str) -> Tuple[int, int, int]:
    """
    Calculate a 3-tuple representing the color in the given hex.

    :param hex_str: the desired color in the format #RRGGBB.
    :return: a 3-tuple of RGB values ``hex_str`` represents
    :raises ValueError: if ``hex_str`` is improperly formatted
    """
    if not is_color(hex_str):
        hex_repr = f"'{hex_str}'" if type(hex_str) is str else str(hex_str)
        raise ValueError(f"Please provide a color in the format '#RRGGBB'. Received {hex_repr}.")

    red = int(hex_str[1:3], 16)
    blue = int(hex_str[3:5], 16)
    green = int(hex_str[5:7], 16)

    return red, blue, green


def even_spread(colors, num_leds):
    """Evenly spreads out the colors across the LEDs in order."""
    pixels = []
    pixels_per_color = math.floor(num_leds / len(colors))
    remainder = num_leds % len(colors)

    for color in colors:
        pixels += [color] * pixels_per_color
    pixels += [colors[0]] * remainder

    return pixels


def spread(colors, num_leds, pixels_per_color):
    """Spreads out the colors across the LEDs in order using the
    specified number of pixels per color."""
    pixels = []

    color_index = 0
    leds_left = num_leds
    while leds_left > 0:
        pixels += [colors[color_index]] * pixels_per_color
        color_index = (color_index + 1) % len(colors)
        leds_left -= pixels_per_color

    return pixels


def shift(current, goal, p):
    """Returns current shifted towards goal by a factor of p (proportion)."""
    return [current[i] + ((goal[i] - current[i]) * p) for i in range(3)]


def rotate_left(pixels, n):
    """Rotates the pixels to the left by n."""
    return pixels[n:] + pixels[:n]


def rotate_right(pixels, n):
    """Rotates the pixels to the right by n."""
    return pixels[-n:] + pixels[:-n]


def scroll_left(pixels, sleep_time, client):
    """Scrolls the pixels around once to the left."""
    for _ in pixels:
        client.put_pixels(pixels)
        time.sleep(sleep_time)
        pixels = rotate_left(pixels, 1)


def scroll_right(pixels, sleep_time, client):
    """Scrolls the pixels around once to the right."""
    for _ in pixels:
        client.put_pixels(pixels)
        time.sleep(sleep_time)
        pixels = rotate_right(pixels, 1)
