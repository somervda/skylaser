from menu import Display,MenuItem
from datetime import datetime
import time
from gpsManager import GPSManager
from gimbalManager import GimbalManager

from starFinder import StarFinder

SETTINGS_JSON = "/home/pi/skylaser/settings.json"



# Initializations
display= Display()
display.showText("Starting SkyLaser...")
gm=GimbalManager(SETTINGS_JSON)

# Need GPS info to initialize the starFinder
display.showText("Getting GPS data...")
gpsManager=GPSManager()
if gpsManager.isValid :
    print(gpsManager.latitude , gpsManager.longitude , gpsManager.altitude , gpsManager.datetime , gpsManager.timestamp)
    gpsInfoText = "Latitude: " + str(gpsManager.latitude)[:7] +"\nLongitude: " + str(gpsManager.longitude)[:7] + "\nDate (GMT): " + str(gpsManager.datetime)[:10] + "\nTime (GMT): " + str(gpsManager.datetime)[11:19]
    print(gpsInfoText)
    display.showText(gpsInfoText)
    time.sleep(2)
else:
    display.showText("       Sky Laser!\nGPS faild\nTry restarting.")
    time.sleep(5)
    exit()
    
sf=StarFinder(SETTINGS_JSON,gpsManager.longitude ,gpsManager.latitude,gpsManager.rtcDateTime,reload=False)

def doStartMenu():
    menuItems = []
    menuItems.append(MenuItem("Planets", 0,"Mars, Jupiter etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Satellites", 1,"The ISS, Moon etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Constellations", 2,"The Big Dipper, Orion etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Stars",3, "Polarus,Betelgeuse , Sirus etc", 0, 0, 0, 0))
    menuItems.append(MenuItem("Setup",4, "", 0, 0, 0, 0))
    menuItems.append(MenuItem("Exit", 5,"", 0, 0, 0, 0))
    display.menuItems = menuItems
    return(display.showMenu())

def doSetup():
    menuItems = []
    menuItems.append(MenuItem("Move to 0,0",0, "", 0, 0, 0, 0))
    menuItems.append(MenuItem("Move to 90,0",0, "", 90, 0, 0, 0))
    menuItems.append(MenuItem("Move to 180,0",0, "", 180, 0, 0, 0))
    menuItems.append(MenuItem("Move to 270,0", 0,"", 270, 0, 0, 0))
    menuItems.append(MenuItem("Move to 0,45",0, "", 0, 45, 0, 0))
    menuItems.append(MenuItem("Move to 90,45",0, "", 90, 45, 0, 0))
    menuItems.append(MenuItem("Move to 180,45",0, "", 180, 45, 0, 0))
    menuItems.append(MenuItem("Move to 270,45",0, "", 270, 45, 0, 0))
    menuItems.append(MenuItem("Move to 0,90", 0,"", 0, 90, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    gm.move(selectedItem.azimuth,selectedItem.altitude)

def doStars():
    
    menuItems = []
    for brightStar in sf.getBrightStars():
        if brightStar.name !="":
            menuItems.append(MenuItem(brightStar.name + " (" + str(brightStar.magnitude) + ")",brightStar.id, "", 0, 0, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    print(selectedItem)
    #Get latest GPS info
    gpsManager.readGPS()
    # Create a timescale and ask the current time.
    ts = load.timescale()
    t = gpsManager.datetime

    myLocation = earth + wgs84.latlon(42.3583 * N, 71.0636 * W)
    # astrometric = myLocation.at(t).observe(mars)
    # alt, az, d = astrometric.apparent().altaz()

    # print(alt)
    # print(az)

    # display.menuItems = menuItems
    # selectedItem = display.showMenu()
    # gm.move(selectedItem.azimuth,selectedItem.altitude)

# Main code





while True:
    print("RTC datetime:",gpsManager.rtcDateTime)
    selectedItem=doStartMenu()
    if selectedItem.name =="Setup":
        doSetup()
    if selectedItem.name =="Stars":
        doStars()
    if selectedItem.name =="Exit":
        exit()

