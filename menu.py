from board import SCL, SDA
import busio
import time
import RPi.GPIO as GPIO

# Set GPIO pins to read menu button values
PINUP=16
PINDOWN=20
PINSELECT=21
GPIO.setup(PINUP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PINSELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Import the SSD1306 module for OLED display on I2C.
# Create the I2C interface.
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw

# i2c = busio.I2C(SCL, SDA)
ssdDisplay = i2c(port=1, address=0x3C)
ssd1309Device = ssd1309(ssdDisplay)
# See draw functions at https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html#module-PIL.ImageDraw

# ssd1306 I2C device parameters
I2CWIDTH=128
I2CHEIGHT=64
I2CWINDOWSIZE=7
I2CFONTHEIGHT=9

class MenuItem():
    def __init__(self,name, description, elevation, bearing, distance, brightness):
        self.name = name
        self.description = description
        self.elevation=elevation
        self.bearing=bearing
        self.distance=distance
        self.brightness = brightness


class Menu:
    def __init__(self,itemList):
        # Note: ssd1306 displays normally have a height=64 and wifdth-128
        self.itemList = itemList
        self.height = I2CHEIGHT
        self.width = I2CWIDTH
        self.windowSize = I2CWINDOWSIZE
        self.background = Image.new(ssd1309Device.mode, ssd1309Device.size, "black")
        self.draw = ImageDraw.Draw(self.background)
        ssd1309Device.display(self.background)
    

    def showMenu(self):
        # display menu on the selected device
        # When the menu is first display it starts displaying from the firstItem in the itemList
        # and the initial window starts from the first item.
        self.selectedItemIndex = 0
        self.windowStartIndex=0
        selectedItem = None
        while selectedItem == None:
            selectedItem=self.processButtonPress()
            if selectedItem == None:
                self.displayMenuOnI2c()
            else:
                return(selectedItem)
            # time.sleep(0.1)


    def processButtonPress(self):
        # Check to see if the up, down or select buttons are pressed, if up or down then change the 
        # relavant selectedItemIndex and windowStartIndex values and redisplay the menu. If the select 
        # button is pressed then return the menuItem selected.
        if GPIO.input(PINUP)==0:
            if self.selectedItemIndex>0:
                self.selectedItemIndex-=1
                if self.selectedItemIndex<self.windowStartIndex:
                    self.windowStartIndex-=1
        if GPIO.input(PINDOWN)==0:
            print("Down")
            if self.selectedItemIndex<(len(self.itemList)-1):
                self.selectedItemIndex+=1
                if self.selectedItemIndex>=self.windowStartIndex+self.windowSize:
                    self.windowStartIndex+=1
        if GPIO.input(PINSELECT)==0:
            return(self.itemList[self.selectedItemIndex])
        return None

    def displaySelectionOnI2c(self,selectedItem):
        print("selected:",selectedItem.name)
        self.draw.rectangle(ssd1309Device.bounding_box, outline="black", fill="black")
        self.draw.text((0, 0), selectedItem.name, fill="white")
        ssd1309Device.display(self.background)
        time.sleep(3)

    def displayMenuOnI2c(self):
        print("displayMenuOnI2c: ",self.selectedItemIndex,self.windowStartIndex)
        self.draw.rectangle(ssd1309Device.bounding_box, outline="black", fill="black")

        for index,item in enumerate(self.itemList[self.windowStartIndex:],start=self.windowStartIndex):
            if index==self.selectedItemIndex:
                selectionIndicator=">"
            else:
                selectionIndicator="   "
            self.draw.text((0, (index - self.windowStartIndex) * I2CFONTHEIGHT),selectionIndicator +  item.name, fill="white")
        ssd1309Device.display(self.background)




