import board
import busio
from digitalio import DigitalInOut
import time
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
from adafruit_minimqtt import MQTT
import adafruit_dotstar

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.1

# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.D5)
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

# Get wifi details and more from a secrets.py file
from secrets import secrets

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

## Setup topic and measurement interval
mqtt_topic = "m4-temperature"
sleep_time = 0.1

def connect(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

def publish(client, userdata, topic, pid):
    # This method is called when the client publishes data to a feed.
#    print("Published to {0} with PID {1}".format(topic, pid))
    return


# Connect to WiFi
wifi.connect()

# Set up a MiniMQTT Client
client = MQTT(
    socket,
    broker=secrets['mqtt-broker'],
    port=1883,
    network_manager=wifi,
)

# Connect callback handlers to client
client.on_connect = connect
client.on_subscribe = subscribe
client.on_publish = publish

print("Attempting to connect to %s" % client.broker)
client.connect()
client.subscribe(mqtt_topic)
client.publish(mqtt_topic, "Hello earthling, logging the temperature!")

while True:
    try:
        temperature = ds18.temperature
        print((ds18.temperature,))
        led[0] = (0, 255, 0) # green
        client.publish(mqtt_topic, temperature)
        time.sleep(0.2)
        led[0] = (255, 0, 0) # red
        time.sleep(sleep_time)
    except Exception as err:
        print('An error occured: {}'.format(err))