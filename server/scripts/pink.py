import time
import opc

numLEDs = 512
client = opc.Client('localhost:7890')

black = [(0, 0, 0)] * numLEDs
pink = [(255, 105, 180)] * numLEDs

# Fade to white
client.put_pixels(black)
client.put_pixels(black)
time.sleep(0.5)
client.put_pixels(pink)
