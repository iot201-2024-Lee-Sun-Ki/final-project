from IO7FuPython import ConfiguredDevice
import json
import time
import uComMgr32

from machine import Pin
fan = Pin(16, Pin.OUT)

def handleCommand(topic, msg):
    global lastPub
    jo = json.loads(str(msg,'utf8'))
    print(jo)
    if ('fan' in jo['d']):
        if jo['d']['fan'] == 'on':
            fan.on()
        else:
            fan.off()
        lastPub = - device.meta['pubInterval']

nic = uComMgr32.startWiFi('kitchen_fan')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)

device.connect()

lastPub = time.ticks_ms() - device.meta['pubInterval']

while True:
    # default is JSON format with QoS 0
    if not device.loop():
        break
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()
        device.publishEvent('status', json.dumps({'d':{'fan': 'on' if fan.value() else 'off'}}))

