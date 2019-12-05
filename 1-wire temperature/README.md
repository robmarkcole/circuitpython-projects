## 1-wire temperature sensor DS18B20
* Project: read temperature, publish over MQTT (via wifi) on the `m4-temperature` topic, and visualise. LED blinks red on each reading.
* [DS18B20 Sensor on adafruit](https://www.adafruit.com/product/374) and [Metro M4 Airlift board](https://shop.pimoroni.com/products/adafruit-metro-m4-express-airlift-wifi-lite)
* DS18B20 is 1-Wire interface Temperature sensor manufactured by Dallas Semiconductor Corp. Requires only one digital pin for two way communication with a microcontroller.
* Circuitpython lib (in bundle) -> https://github.com/adafruit/Adafruit_CircuitPython_DS18X20 and [guide](https://learn.adafruit.com/using-ds18b20-temperature-sensor-with-circuitpython). Use [this example](https://github.com/adafruit/Adafruit_CircuitPython_DS18X20/blob/master/examples/ds18x20_simpletest.py)
* Wire to 5V, GND and D5 digital. 4.7 kohm pull-up resistor required between digital and 5V (I only had and used 10 kohm)
* Requirements: use a `secrets.py`, and setup the measurement parameters in `config.py`
* MQTT broker - I am using [mosquitto](https://github.com/eclipse/mosquitto)
* chart data - I am using [MQTT explorer](https://mqtt-explorer.com/) to visualise the MQTT readings. You can also chart data in Mu as shown below:

* **Issue**: suffering intermittent wifi issue `An error occured: Failed to send 2 bytes (sent 0)`, so on an exception am resetting the wifi connection.

<p align="center">
<img src="https://github.com/robmarkcole/circuitpython-projects/blob/master/1-wire%20temperature/1wire-setup.jpg" width="700">
</p>

<p align="center">
<img src="https://github.com/robmarkcole/circuitpython-projects/blob/master/1-wire%20temperature/mu.jpg" width="700">
</p>

<p align="center">
<img src="https://github.com/robmarkcole/circuitpython-projects/blob/master/1-wire%20temperature/MQTT-Explorer.jpg" width="700">
</p>

## Optional - Home Assistant display
Using [Home Assistant](https://www.home-assistant.io/) allows you to integrate the sensor readings into your daily life. Display readings in Home Assistant using an [MQTT sensor](https://www.home-assistant.io/integrations/sensor.mqtt/), add to your `sensors.yaml`
```yaml
- platform: mqtt
  name: m4-temperature
  state_topic: m4-temperature
  unit_of_measurement: '°C'
```

<p align="center">
<img src="https://github.com/robmarkcole/circuitpython-projects/blob/master/1-wire%20temperature/hass-m4-temperature.jpg" width="400">
</p>