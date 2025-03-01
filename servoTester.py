from adafruit_servokit import ServoKit
import time
from settingsManager import SettingsManager
settingsManager=SettingsManager("settings.json")
kit = ServoKit(channels=16)
# servo 0 is azamuth
kit.servo[0].set_pulse_width_range(settingsManager.get_setting("AZAMUTH_MIN"), settingsManager.get_setting("AZAMUTH_MAX"))
# Servo 1 is altitude
kit.servo[1].set_pulse_width_range(700, 2500)
while True:
    kit.servo[1].angle = 0
    # rangle = 0
    time.sleep(2)
    kit.servo[0].angle = 0
    time.sleep(1)
    # kit.servo[1].angle = 0
    print(0,0)
    time.sleep(3)
    kit.servo[0].angle = 45
    time.sleep(3)
    kit.servo[0].angle = 90
    time.sleep(3)
    kit.servo[0].angle = 135
    time.sleep(3)
    kit.servo[0].angle = 180
    # time.sleep(1)
    # kit.servo[1].angle = 180
    print(0,180)
    time.sleep(3)
# while True:
#     if rangle>180:
#         rangle=0
#     dangle = 0
#     while True:
#         if dangle>180:
#             dangle=0
#             break
#         print(rangle,dangle)
#         kit.servo[0].angle = rangle
#         kit.servo[1].angle = dangle
#         if dangle==0:
#             time.sleep(1)
#         dangle +=5
#         time.sleep(.1)
#     rangle +=5

