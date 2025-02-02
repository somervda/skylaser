from i2c_hmc5883l import HMC5883
from time import sleep

i2c_HMC5883l = HMC5883(gauss=1.3)
i2c_HMC5883l.set_declination(0, 0)

while True:
   print(i2c_HMC5883l.get_heading())
   sleep(1)