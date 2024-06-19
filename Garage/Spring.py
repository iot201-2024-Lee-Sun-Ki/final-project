from IO7FuPython import ConfiguredDevice
import json
import time
import uComMgr32

def handleCommand(topic, msg):
    global lastPub
    jo = json.loads(str(msg,'utf8'))
    if ("valve" in jo['d']):
        if jo['d']['valve'] is 'on':
            valve.on()
        else:
            valve.off()
        lastPub = - device.meta['pubInterval']

nic = uComMgr32.startWiFi('va')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)

device.connect()

from machine import Pin
valve = Pin(43, Pin.OUT)
lastPub = time.ticks_ms() - device.meta['pubInterval']

while True:
    # default is JSON format with QoS 0
    if not device.loop():
        break
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()
        device.publishEvent('status', json.dumps({'d':{'valve': 'on' if valve.value() else 'off'}}))


