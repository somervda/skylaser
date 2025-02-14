import gy271compass as GY271
from time import sleep

#  i2cdetect -y 1

sensor = GY271.compass(address=0x0d)
# sensor.calibrate()
sensor.set_declination(0)

while True:
    print(sensor.get_bearing(-3127,3740,-5397,0))
    # print(sensor.getRaw())
    # print(sensor.read_temp())
    sleep(1)