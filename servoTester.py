from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
kit.servo[15].set_pulse_width_range(650, 2600)
angle = 0
while True:
    angle +=3
    if angle>180:
        angle=0
    kit.servo[15].angle = angle
    print(angle)
    time.sleep(.3)

