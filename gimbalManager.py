from settingsManager import SettingsManager
from adafruit_servokit import ServoKit
import time

class GimbalManager:
    def __init__(self):
        self.settingsManager = SettingsManager("settings.json")
        self.kit = ServoKit(channels=16)
        # Set the gimbals range of motion to be 180 degrees, starting with 0 degrees pointing east
        # and degrees increasing in anti-clockwise direction. Servo 0 controls the azimuth on the gimbal
        self.kit.servo[0].set_pulse_width_range(self.settingsManager.get_setting("AZAMUTH_MIN"), self.settingsManager.get_setting("AZAMUTH_MAX"))
        # Set the range of motion for the altitude on the gimbal. Set it to be 180 degrees with 0 degrees being the horezontal position
        # Servo 1 controls the altitude of the gimbal
        self.kit.servo[1].set_pulse_width_range(self.settingsManager.get_setting("ALTITUDE_MIN"), self.settingsManager.get_setting("ALTITUDE_MAX"))

    def move(self,azimuth,altitude):
        # Perform translation of the azumuth and  altitude into setting the servos on the gimbal will use. I do the translation based on the
        # quadrent the azimuth is set to, each quadrent needs different translation process to result in being able to position the 
        # gimbal being able to point to a specific point in the sky.
        # Note: this is becouse the ginbal is set to rotate a maximum of 180 degrees and the altitude can also rotate just 180 degrees
        servoAzimuth=0
        servoAltitude=0
        if azimuth >=0 and azimuth<=90:
            servoAzimuth=90-azimuth
            servoAltitude=altitude
        if azimuth >=270 and azimuth<=360:
            servoAzimuth=450-azimuth
            servoAltitude=altitude
        if azimuth >90 and azimuth<=270:
            servoAzimuth=270-azimuth
            servoAltitude=180-altitude
        print("azimuth:",azimuth," altitude:",altitude," servoAzimuth:",servoAzimuth," servoAltitude:",servoAltitude)
        self.kit.servo[0].angle=servoAzimuth
        self.kit.servo[1].angle=servoAltitude
        time.sleep(1.5)

if __name__ == "__main__":
    gm=GimbalManager()
    # 1=altitude 2=azumuth 3=full
    TEST_TYPE = 1
    gm.move(0,0)
    time.sleep(5)
    if TEST_TYPE == 1:
        # Altitude
        for loop in range(3):
            gm.move(90,0)
            gm.move(270,0)

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

