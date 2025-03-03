from gimbalManager import GimbalManager
import time

gm=GimbalManager("skylaser/settings.json")
# 1=altitude 2=azumuth 3=full
TEST_TYPE = 2
gm.move(0,0)
time.sleep(5)
if TEST_TYPE == 1:
    # Altitude
    for loop in range(3):
        gm.move(0,0)
        gm.move(0,45)
        gm.move(0,90)
        gm.move(180,45)
        gm.move(180,0)

if TEST_TYPE == 2:
    # AZIMUTH
    for loop in range(2):
        for azimuth in range(0,360,45):
            gm.move(azimuth,0)

if TEST_TYPE == 3:
    for azimuth in range(0,360,45):
        for altitude in range(0,100,45):
            gm.move(azimuth,altitude)


gm.move(0,0)