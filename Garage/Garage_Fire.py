from machine import Pin
from IO7FuPython import Device, ConfiguredDevice
import json, time, uComMgr32
import neopixel

FLAME_SENSOR_PIN = 15
flame_sensor = Pin(FLAME_SENSOR_PIN, Pin.IN)
flame_detected = flame_sensor.value()


neopxl = neopixel.NeoPixel(Pin(22), 8, bpp=3)
color = {'r':0, 'g':0, 'b':0}

def setPixel(color):
    for i in range(8):
        neopxl[i] = (color['r'], color['g'], color['b'])
    neopxl.write()
       
def handleCommand(topic, msg):
    global lastPub, color
    jo = json.loads(str(msg,'utf8'))
    if ("color" in jo['d']):
        color = jo['d']['color']
        print(color)
        setPixel(color)   
    lastPub = - device.meta['pubInterval']
        
        
nic = uComMgr32.startWiFi('fire')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)
device.connect()
lastPub = time.ticks_ms() - device.meta['pubInterval']
setPixel(color)

while True:
    if not device.loop():
        break
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()
       # device.publishEvent('status', json.dumps({'d':{'color': color}}))	
        device.publishEvent('status', json.dumps({'d':{'fire': 'off' if flame_sensor.value() else 'on'}}))
        #device.publishEvent('status', json.dumps({'d':{'valve': 'on' if led.value() else 'off'}}))
        
        
    if flame_sensor.value() == 0:
        print("불꽃이 감지되었습니다!")
    else:
        print("불꽃이 감지되지 않았습니다.")
        
    time.sleep(2)


