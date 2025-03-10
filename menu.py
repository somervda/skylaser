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
    def __init__(self,name,id, description, azimuth,altitude,  distance, brightness):
        self.name = name
        self.id = id
        self.description = description
        self.azimuth=azimuth
        self.altitude=altitude
        self.distance=distance
        self.brightness = brightness


class Display:
    def __init__(self):
        # Note: ssd1306 displays normally have a height=64 and width-128
        self._menuItems = []
        self._height = I2CHEIGHT
        self._width = I2CWIDTH
        self._windowSize = I2CWINDOWSIZE
        self._background = Image.new(ssd1309Device.mode, ssd1309Device.size, "black")
        self._draw = ImageDraw.Draw(self._background)
        ssd1309Device.display(self._background)

    @property
    def menuItems(self): 
        return self._menuItems


    @menuItems.setter 
    def menuItems(self,menuItems):
        self._menuItems = menuItems

    def showMenu(self):
        # display menu on the selected device
        # When the menu is first display it starts displaying from the firstItem in the menuItems
        # and the initial window starts from the first item.
        self._selectedItemIndex = 0
        self._windowStartIndex=0
        selectedItem = None
        # Wait for PINSELECT to return to unpressed position
        while GPIO.input(PINSELECT)==0:
            time.sleep(0.1)
        while selectedItem == None:
            selectedItem=self.processButtonPress()
            if selectedItem == None:
                self.displayMenu()
            else:
                return(selectedItem)



    def processButtonPress(self):
        # Check to see if the up, down or select buttons are pressed, if up or down then change the 
        # relavant selectedItemIndex and windowStartIndex values and redisplay the menu. If the select 
        # button is pressed then return the menuItem selected.
        if GPIO.input(PINUP)==0:
            if self._selectedItemIndex>0:
                self._selectedItemIndex-=1
                if self._selectedItemIndex<self._windowStartIndex:
                    self._windowStartIndex-=1
        if GPIO.input(PINDOWN)==0:
            print("Down")
            if self._selectedItemIndex<(len(self._menuItems)-1):
                self._selectedItemIndex+=1
                if self._selectedItemIndex>=self._windowStartIndex+self._windowSize:
                    self._windowStartIndex+=1
        if GPIO.input(PINSELECT)==0:
            return(self._menuItems[self._selectedItemIndex])
        return None

    def showSelection(self,selectedItem):
        # print("showSelection:",selectedItem.name)
        self.showText(selectedItem.name + "\n" + selectedItem.description)

    def displayMenu(self):
        # print("displayMenu: ",self._selectedItemIndex,self._windowStartIndex)
        self._draw.rectangle(ssd1309Device.bounding_box, outline="black", fill="black")

        for index,item in enumerate(self._menuItems[self._windowStartIndex:],start=self._windowStartIndex):
            if index==self._selectedItemIndex:
                selectionIndicator=">"
            else:
                selectionIndicator="   "
            self._draw.text((0, (index - self._windowStartIndex) * I2CFONTHEIGHT),selectionIndicator +  item.name, fill="white")
        ssd1309Device.display(self._background)
    
    def showText(self,text,x=0,y=0):
        # print("showText:")
        self._draw.rectangle(ssd1309Device.bounding_box, outline="black", fill="black")
        self._draw.multiline_text((x, y), text, fill="white")
        ssd1309Device.display(self._background)


if __name__ == "__main__":
    display= Display()

    menuItems = []
    menuItems.append(MenuItem("Planets",0, "The Planets", 0, 0, 0, 0))
    menuItems.append(MenuItem("Satellites",0, "The ISS, Moon etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Constellations",0, "The big dipper, orion etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Stars",0, "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Setup",0, "", 0, 0, 0, 0))


    print(len(menuItems))
    display= Display()
    display.menuItems = menuItems
    s=display.showMenu()
    display.showSelection(s)
    time.sleep(1.5)
    display.showText("Thats all folks!")
    time.sleep(1.5)
