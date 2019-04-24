import re
import math

from typing import Tuple, List, Iterable


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
        raise ValueError("Please provide a color in the format '#RRGGBB'. "
                         f"Received {hex_repr}.")

    red = int(hex_str[1:3], 16)
    blue = int(hex_str[3:5], 16)
    green = int(hex_str[5:7], 16)

    return red, blue, green


def even_spread(colors: List, num_leds: int) -> List:
    """
    Evenly spread out the colors across the LEDs in order.

    :param colors: a list of values to spread
    :param num_leds: the length of the list to create from the given colors
    :return: a list consisting of ``colors`` spread across ``num_leds`` indices
    :raises ValueError: if ``colors`` is empty or ``num_leds`` is negative
    """
    if len(colors) < 1:
        raise ValueError('no colors provided')
    if num_leds < 0:
        raise ValueError('cannot spread across a negative number of LEDs')

    pixels = []
    pixels_per_color = math.floor(num_leds / len(colors))
    remainder = num_leds % len(colors)

    for color in colors:
        pixels += [color] * pixels_per_color
    pixels += [colors[0]] * remainder

    return pixels


def spread(colors: List, num_leds: int, pixels_per_color: int):
    """
    Spread out the colors across the LEDs in order using the specified number
    of pixels per color.

    :param colors: the values to spread
    :param num_leds: the length of the list to create from the given colors
    :param pixels_per_color: the length of each color sequence
    :return: a list consisting of sequences of values in ``colors`` of length
       ``pixels_per_color`` each
    :raises ValueError: if ``colors`` is empty or either ``num_leds`` or
        ``pixels_per_color`` is negative
    """
    if len(colors) < 1:
        raise ValueError('no colors provided')
    if num_leds < 0 or pixels_per_color < 0:
        raise ValueError('cannot spread across a negative number of LEDs')

    pixels = []
    color_index = 0
    leds_left = num_leds
    while leds_left > 0:
        pixels += [colors[color_index]] * min(pixels_per_color, leds_left)
        color_index = (color_index + 1) % len(colors)
        leds_left -= pixels_per_color

    return pixels


def shift(current: Iterable[float], goal: Iterable[float],
          p: float) -> Iterable[float]:
    """
    Shift a color towards another.

    :param current: a 3-tuple representing the starting color
    :param goal: a 3-tuple representing the color to shift towards
    :param p: a value indicating how far to shift (0 => no shift, 1 => ``goal``)
    :return: the shifted color
    """
    return tuple([c + ((g - c) * p) for c, g in zip(current, goal)])


def rotate_left(l: List, n: int):
    """
    Generate a version of the given list rotated left.

    :param l: the list to rotate
    :param n: how many spaces to rotate the list
    :return: the rotated list
    """
    n %= len(l)
    return l[n:] + l[:n]


def rotate_right(l: List, n: int):
    """
    Generate a version of the given list rotated right

    :param l: the list to rotate
    :param n: how many spaces to rotate the list
    :return: the rotated list
    """
    n %= len(l)
    return l[-n:] + l[:-n]
