from machine import Pin
from IO7FuPython import Device, ConfiguredDevice
import json, time, uComMgr32

FLAME_SENSOR_PIN = 15
flame_sensor = Pin(FLAME_SENSOR_PIN, Pin.IN)
flame_detected = flame_sensor.value()
       
def handleCommand(topic, msg):
   pass
           
nic = uComMgr32.startWiFi('fire')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)
device.connect()
lastPub = time.ticks_ms() - device.meta['pubInterval']

while True:
    if not device.loop():
        break
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()   
        device.publishEvent('status', json.dumps({'d':{'flame': 'off' if flame_sensor.value() else 'on'}}))
        
    if flame_sensor.value() == 0:
        print("불꽃이 감지되었습니다!")
    else:
        print("불꽃이 감지되지 않았습니다.")
        
    time.sleep(2)




