import board
import analogio
import neopixel
import time

photocell = analogio.AnalogIn(board.A0)
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3

while True:
    #print("test")
    #print(photocell.value)
    reading = photocell.value
    print((reading, 0))
    if reading > 30000:
        led[0] = (255, 0, 0)
    else:
        led[0] = (0, 255, 0)
    time.sleep(0.1)