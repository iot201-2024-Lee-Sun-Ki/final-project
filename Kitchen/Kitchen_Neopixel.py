from IO7FuPython import Device, ConfiguredDevice
import json, time, ComMgr
import neopixel
from machine import Pin

neopixel = neopixel.NeoPixel(Pin(15), 8, bpp=3)
color = {'r' : 0, 'g' : 0, 'b' : 0}

def setPixel(color):
    for i in range(8):
        neopixel[i] = (color['r'], color['g'], color['b'])
    neopixel.write()
    
def handleCommand(topic, msg):
    global lastPub, color
    jo = json.loads(str(msg, 'utf8'))
    if ("color" in jo['d']):
        color = jo['d']['color']
        setPixel(color)
        print(color)
        lastPub = - device.meta['pubInterval']

nic = ComMgr.startWiFi('kitchen_neopixel')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)
device.connect()

lastPub = time.ticks_ms() - device.meta['pubInterval']
setPixel(color)

while True:
    device.loop()
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()
        device.publishEvent('status', json.dumps({'d':{'color':color}}))



