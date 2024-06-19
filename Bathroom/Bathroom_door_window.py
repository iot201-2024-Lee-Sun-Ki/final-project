from IO7FuPython import ConfiguredDevice
import json
import time
import uComMgr32
from machine import Pin, PWM
import time

# 서보모터의 PWM 핀 설정 (예: GPIO 15)
servo_pin = Pin(15)
servo_pwm = PWM(servo_pin, freq=50 , duty=0)  # 서보모터는 일반적으로 50Hz 주파수를 사용
servo_pin1 = Pin(16)
servo_pwm1 = PWM(servo_pin1, freq=50 , duty=0)

# 각도 -> 듀티사이클 변환 함수
def set_servo_angle(angle):
    global servo_pwm
    servo_pwm.duty(int(((angle+90) * 2 /180 +0.5) / 20 *1023))
def set_servo_angle1(angle):
    global servo_pwm1
    servo_pwm1.duty(int(((angle+90) * 2 /180 +0.5) / 20 *1023))
    
def handleCommand(topic, msg):
    global lastPub,angle,angle1
    jo = json.loads(str(msg,'utf8'))
    if ("door" in jo['d']):
        if jo['d']['door'] is 'open':
            angle = 90
            set_servo_angle(-angle)
        else:
            angle = 45
            set_servo_angle(-angle)
    
    if ("window" in jo['d']):
        if jo['d']['window'] is 'open':
            angle1 = 90
            set_servo_angle1(-angle1)
        else:
            angle1 = 45
            set_servo_angle1(-angle1)
    lastPub = - device.meta['pubInterval']
 

nic = uComMgr32.startWiFi('io7thermostat')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)

device.connect()

lastPub = time.ticks_ms() - device.meta['pubInterval']
angle = 0
angle1 = 0


while True:
    # default is JSON format with QoS 0
    if not device.loop():
        break
    if (time.ticks_ms() - device.meta['pubInterval']) > lastPub:
        lastPub = time.ticks_ms()
        if angle == 90:
            device.publishEvent('status', json.dumps({'d':{'door': 'open'}}))
        elif angle == 45:
            device.publishEvent('status', json.dumps({'d':{'door': 'close'}}))
        if angle1 == 90:
            device.publishEvent('status', json.dumps({'d':{'window': 'open'}}))
        elif angle1 == 45:
            device.publishEvent('status', json.dumps({'d':{'window': 'close'}}))