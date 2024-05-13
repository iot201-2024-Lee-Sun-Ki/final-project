influxdb example
========

### io7uThermometer

```python
from IO7FuPython import ConfiguredDevice
import json
import time
import uComMgr32
from machine import Pin, ADC, Timer
import s3lcd
import tft_config
import vga2_8x16 as font1
import vga1_bold_16x32 as font2
import dht

sensor = dht.DHT22(Pin(17))

temerature = 0
humidity = 0

tft = tft_config.config(3)

tft.init()
tft.fill(s3lcd.BLACK)
tft.text(font2, 'Thermometer', 85, 5, s3lcd.WHITE)
tft.text(font1, 'Temperature : ', 65, 80, s3lcd.WHITE)
tft.text(font1, 'Humidity    : ', 65, 110, s3lcd.WHITE)
tft.show()

lastMeasured = -2001
def measureData():
    global temperature, humidity, lastMeasured
    if (time.ticks_ms() - 2000) > lastMeasured:
        lastMeasured = time.ticks_ms()
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        display()

def handleCommand(topic, msg):
    global lastPub
    jo = json.loads(str(msg,'utf8'))
    if ("status" in jo['d']):
        lastPub = - device.meta['pubInterval']
        display()
        
def display():
    tft.text(font1, f'{round(temperature, 2)}', 200, 80, s3lcd.WHITE)
    tft.text(font1, f'{round(humidity, 2)}', 200, 110, s3lcd.WHITE)
    tft.show()
    
nic = uComMgr32.startWiFi('io7thermometer')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)

device.connect()

lastPub = time.ticks_ms() - device.meta['pubInterval']

while True:
    if not device.loop():
        tft.deinit()
        break
    measureData()
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()
        device.publishEvent('status',
            json.dumps({
                'd' : {
                        'temperature' : round(temperature, 2),
                        'humidity' : round(humidity, 2),
                      }
                 }
            )
        )


```