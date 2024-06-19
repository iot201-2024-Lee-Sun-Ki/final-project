from IO7FuPython import ConfiguredDevice
import json
import time
import uComMgr32
from machine import Pin, ADC, Timer
import dht

sensor = dht.DHT22(Pin(13))
valve = Pin(12, Pin.OUT)


temerature = 0
humidity = 0


def t2r(t):
    # 0.1960784 = (60 - 10) / 255 - 0
    # 
    return (t - 10) / 0.1960784

lastMeasured = 0
def measureData():
    global temperature, humidity, lastMeasured
    if (time.ticks_ms() - 2000) > lastMeasured:
        lastMeasured = time.ticks_ms()
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

def handleCommand(topic, msg):
    global lastPub, value
    jo = json.loads(str(msg,'utf8'))
    if ("valve" in jo['d']):
        if jo['d']['valve'] is 'on':
            valve.on()
        else:
            valve.off()
        
    
    if ("temperature" in jo['d']):
        value = t2r(int(jo['d']['temperature']))
        
        lastPub = - device.meta['pubInterval']
        
        
        
nic = uComMgr32.startWiFi('io7thermostat')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)

device.connect()

lastPub = time.ticks_ms() - device.meta['pubInterval']

while True:
    if not device.loop():
        break
    measureData()
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()
        if temperature is not None:
            device.publishEvent('status',
                json.dumps({
                    'd' : {
                            'temperature' : round(temperature, 2),
                            'humidity' : round(humidity, 2),
                          }
                     }
                )
            )
        device.publishEvent('status', json.dumps({'d':{'valve': 'on' if valve.value() else 'off'}}))


