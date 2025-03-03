from menu import Display,MenuItem
from datetime import datetime
import time
from gpsManager import GPSManager
from gimbalManager import GimbalManager

from skyfield.api import load

# Initializations
gpsManager=GPSManager()
display= Display()
gm=GimbalManager("/home/pi/skylaser/settings.json")

def doStartMenu():
    menuItems = []
    menuItems.append(MenuItem("Planets", "Mars, Jupiter etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Satellites", "The ISS, Moon etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Constellations", "The Big Dipper, Orion etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Stars", "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Setup", "", 0, 0, 0, 0))
    menuItems.append(MenuItem("Exit", "", 0, 0, 0, 0))
    display.menuItems = menuItems
    return(display.showMenu())

def doSetup():
    menuItems = []
    menuItems.append(MenuItem("Move to 0,0", "", 0, 0, 0, 0))
    menuItems.append(MenuItem("Move to 90,0", "", 90, 0, 0, 0))
    menuItems.append(MenuItem("Move to 180,0", "", 180, 0, 0, 0))
    menuItems.append(MenuItem("Move to 270,0", "", 270, 0, 0, 0))
    menuItems.append(MenuItem("Move to 0,45", "", 0, 45, 0, 0))
    menuItems.append(MenuItem("Move to 90,45", "", 90, 45, 0, 0))
    menuItems.append(MenuItem("Move to 180,45", "", 180, 45, 0, 0))
    menuItems.append(MenuItem("Move to 270,45", "", 270, 45, 0, 0))
    menuItems.append(MenuItem("Move to 0,90", "", 0, 90, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    gm.move(selectedItem.azimuth,selectedItem.altitude)

def doStars():
    # Get latest GPS info
    gpsManager.readGPS()
    # Create a timescale and ask the current time.
    ts = load.timescale()
    t = gpsManager.datetime
    
    menuItems = []
    menuItems.append(MenuItem("Move to 0,0", "", 0, 0, 0, 0))

    display.menuItems = menuItems
    selectedItem = display.showMenu()
    gm.move(selectedItem.azimuth,selectedItem.altitude)

# Main code

gpsManager=GPSManager()

display.showText("       Sky Laser!\nGetting GPS data...")
time.sleep(2)

if gpsManager.readGPS() :
    print(gpsManager.latitude , gpsManager.longitude , gpsManager.altitude , gpsManager.datetime , gpsManager.timestamp)
    gpsInfoText = "Latitude: " + str(gpsManager.latitude)[:7] +"\nLongitude: " + str(gpsManager.longitude)[:7] + "\nDate (GMT): " + str(gpsManager.datetime)[:10] + "\nTime (GMT): " + str(gpsManager.datetime)[11:19]
    print(gpsInfoText)
    display.showText(gpsInfoText)
    time.sleep(2)
else:
    display.showText("       Sky Laser!\nGPS faild\nTry restarting.")
    time.sleep(5)
    exit()

while True:
    selectedItem=doStartMenu()
    if selectedItem.name =="Setup":
        doSetup()
    if selectedItem.name =="Stars":
        doStars()
    if selectedItem.name =="Exit":
        exit()

