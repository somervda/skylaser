import gy271compass as GY271
from time import sleep

#  i2cdetect -y 1

sensor = GY271.compass(address=0x0d)
sensor.set_declination(0)

while True:
    print(sensor.get_bearing())
    sleep(1)