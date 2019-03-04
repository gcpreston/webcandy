import time
import opc

numLEDs = 512
client = opc.Client('localhost:7890')

black = [(0, 0, 0)] * numLEDs
white = [(65, 105, 225)] * numLEDs

# Fade to white
client.put_pixels(black)
client.put_pixels(black)
time.sleep(0.5)
client.put_pixels(white)
