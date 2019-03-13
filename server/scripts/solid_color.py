import sys
import time
import opc


def get_color(args):
    if len(args) != 2:
        raise ValueError('Please provide a color in the format #RRGGBB.')

    color_str = args[-1]
    red = int(color_str[1:3], 16)
    blue = int(color_str[3:5], 16)
    green = int(color_str[5:7], 16)

    return tuple([red, blue, green])


def main(args):
    num_leds = 512
    client = opc.Client('localhost:7890')

    black = [(0, 0, 0)] * num_leds
    color = [get_color(args)] * num_leds

    client.put_pixels(black)
    client.put_pixels(black)
    time.sleep(0.5)
    client.put_pixels(color)


if __name__ == '__main__':
    main(sys.argv)
