from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
kit.servo[1].set_pulse_width_range(700, 2400)
rangle = 0
kit.servo[0].angle = 0
time.sleep(1)
kit.servo[1].angle = 0
print(0,0)
time.sleep(10)
kit.servo[0].angle = 180
time.sleep(1)
kit.servo[1].angle = 90
print(180,180)
time.sleep(10)
while True:
    if rangle>180:
        rangle=0
    dangle = 0
    while True:
        if dangle>90:
            dangle=0
            break
        print(rangle,dangle)
        kit.servo[0].angle = rangle
        kit.servo[1].angle = dangle
        if dangle==0:
            time.sleep(1)
        dangle +=5
        time.sleep(.1)
    rangle +=5

