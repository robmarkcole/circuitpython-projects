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
from secrets import secrets
from config import config

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.1

GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.D5)
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

def connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

def publish(client, userdata, topic, pid):
#    print("Published to {0} with PID {1}".format(topic, pid))
    return

wifi.connect()
print("Connected to wifi with IP {}".format(wifi.ip_address()))

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
client.connect()

while True:
    try:
        temperature = ds18.temperature
        print((ds18.temperature,))
        led[0] = GREEN
        client.publish(config['mqtt_topic'], temperature)
        time.sleep(0.1)
        led[0] = RED
        time.sleep(config['sleep_time'])
    except Exception as err:
        print('An error occured: {}'.format(err))
        wifi.reset()
        wifi.connect()