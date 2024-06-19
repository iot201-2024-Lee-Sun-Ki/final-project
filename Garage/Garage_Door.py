import time
import json
from machine import Pin, PWM
from hcsr04 import HCSR04
from uComMgr32 import startWiFi
from IO7FuPython import ConfiguredDevice

# HCSR04 센서 설정
sensor1 = HCSR04(trigger_pin=19, echo_pin=21, echo_timeout_us=10000)
sensor2 = HCSR04(trigger_pin=22, echo_pin=23, echo_timeout_us=10000)

# 서보모터 설정
servo_pin = Pin(15)
servo_pwm = PWM(servo_pin, freq=50)

# 거리 측정 함수
def measure_distance1():
    distance = sensor1.distance_cm()
    print('Distance1:', distance, 'cm')
    return distance

def measure_distance2():
    distances = []
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 5000:  # 5초 동안 측정
        distance = sensor2.distance_cm()
        print('Distance2:', distance, 'cm')
        if distance is not None:
            distances.append(distance)
        time.sleep(1)  # 잠시 대기
    if distances:
        average_distance = sum(distances) / len(distances)
        return average_distance
    else:
        return None

# 각도 -> 듀티사이클 변환 함수
def set_servo_angle(angle):
    min_duty = 26   # 최소 듀티사이클 값 (서보모터의 0도 위치)
    max_duty = 123  # 최대 듀티사이클 값 (서보모터의 180도 위치)
    duty = int(min_duty + (angle / 180.0) * (max_duty - min_duty))
    servo_pwm.duty(duty)
    print(f'Servo angle set to {angle} degrees, duty: {duty}')

# 명령 처리 함수
def handleCommand(topic, msg):
    global lastPub, angle
    jo = json.loads(msg.decode('utf-8'))
    print(jo)
    if ("mot" in jo['d']):
        if jo['d']['mot'] == 'off':
            angle = 1
            print("문이 닫힙니다.")
            
        else:
            angle = 90
            print("문이 열립니다.")

        set_servo_angle(angle)
        
        lastPub = time.ticks_ms() - device.meta['pubInterval']  # Update lastPub

# WiFi 연결 및 장치 설정
nic = startWiFi('iot')
device = ConfiguredDevice()
device.setUserCommand(handleCommand)
device.connect()
lastPub = time.ticks_ms() - device.meta['pubInterval']

# 메인 루프
while True:
    if not device.loop():
        break
    if (time.ticks_ms() - lastPub) > device.meta['pubInterval']:
        lastPub = time.ticks_ms()
        distance1 = measure_distance1()  # 첫 번째 센서로부터의 거리 측정
        distance2 = measure_distance2()  # 두 번째 센서로부터의 거리 측정
        if distance1 is not None and distance2 is not None:
            device.publishEvent('status', json.dumps({'d': {'distance1': distance1, 'distance2': distance2}}))
    time.sleep(1)

