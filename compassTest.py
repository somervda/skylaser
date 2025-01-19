import gy271compass as GY271
from time import sleep

sensor = GY271.compass(address=0x0d)

while True:
    print(sensor.get_bearing())
    sleep(1)