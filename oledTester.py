# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
from board import SCL, SDA
import busio
import time

# Import the SSD1306 module.
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
print(i2c.scan())

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
#  128 * 64 ssd1309
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
# display.poweron()
# display.contrast(255)
# Alternatively you can change the I2C address of the device with an addr parameter:
#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
display.fill(0)

display.show()

# Set a pixel in the origin 0,0 position.
# display.pixel(0, 0, 1)
# Set a pixel in the middle 64, 16 position.
# display.pixel(64, 16, 1)
# Set a pixel in the opposite 127, 31 position.
# display.pixel(127, 31, 1)
# display.fill_rect(25, 2, 20, 10, True)
display.text("Planets", 0, 0,1)
display.text("Stars", 0, 10,1)
display.text("Constalations", 0, 20,1)
display.text("Satalites", 0, 30,1)
display.show()
time.sleep(5)
display.fill(0)
display.show()
