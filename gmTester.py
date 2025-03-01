from gimbalManager import GimbalManager
gm=GimbalManager()
for azimuth in range(0,360,45):
    for altitude in range(0,100,45):
        gm.move(azimuth,altitude)
gm.move(0,90)