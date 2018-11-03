# Trinket M0
import board
import analogio
import digitalio
import time

photocell = analogio.AnalogIn(board.A0)
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

while True:

    reading = photocell.value
    print((reading, 0))
    if reading > 30000:
        led.value = True
    else:
        led.value = False
    time.sleep(0.1)