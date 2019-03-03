import time
from . import opc

numLEDs = 512
client = opc.Client('localhost:7890')

black = [(0, 0, 0)] * numLEDs
yellow = [(255, 255, 153)] * numLEDs

client.put_pixels(black)
client.put_pixels(black)
time.sleep(0.5)
client.put_pixels(yellow)
