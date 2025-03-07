import time
from menu import Display,MenuItem
from datetime import datetime
from gpsManager import GPSManager
from gimbalManager import GimbalManager
from celestialManager import CelestialManager
from settingsManager import SettingsManager

print("\n\nStarting Skylaser")

# Initializations
display= Display()
display.showText("Starting SkyLaser...")
gm=GimbalManager()
settingsManager=SettingsManager("settings.json")

# Need GPS info to initialize the starFinder
display.showText("Getting GPS data...")
gpsManager=GPSManager()
if gpsManager.isValid :
    print(gpsManager.latitude , gpsManager.longitude , gpsManager.elevation , gpsManager.datetime , gpsManager.timestamp)
    gpsInfoText = "Latitude: " + str(gpsManager.latitude)[:7] +"\nLongitude: " + str(gpsManager.longitude)[:7] + "\nDate (GMT): " + str(gpsManager.datetime)[:10] + "\nTime (GMT): " + str(gpsManager.datetime)[11:19] 
    print(gpsInfoText)
    display.showText(gpsInfoText)
    time.sleep(2)
else:
    display.showText("       Sky Laser!\nGPS faild\nTry restarting.")
    time.sleep(5)
    exit()

display.showText("Loading celestial data...")  
cm=CelestialManager(gpsManager.latitude,gpsManager.longitude ,gpsManager.elevation,gpsManager.rtcDateTime,reload=False)

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
    for brightStar in cm.brightStars:
        menuItems.append(MenuItem(brightStar.name + " (" + str(brightStar.magnitude) + ")",brightStar.id, "", brightStar.azimuth, brightStar.altitude, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    print(selectedItem)
    # Get the objects most recent information on azimuth and altitude.
    starCoordinates=cm.getHipApparantCoordinate(selectedItem.id,gpsManager.rtcDateTime)
    print(starCoordinates)
    actionText=selectedItem.name  + "\nAzimuth: " + str(starCoordinates.get("azimuth").degrees)[:4] + "\nAltitude: " + str(starCoordinates.get("altitude").degrees)[:4] 
    display.showText(actionText)
    gm.move(starCoordinates.get("azimuth").degrees,starCoordinates.get("altitude").degrees)
    time.sleep(5)

def doConstellations():
    menuItems = []
    for constellation in cm.constellations:
        # Only show constellations that are abouve the horizon
        if constellation.altitude>settingsManager.get_setting("CONSTELLATION_ALTITUDE_CUTOFF"):
            menuItems.append(MenuItem(constellation.name ,constellation.hipId, constellation.description, constellation.azimuth, constellation.altitude, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    print(selectedItem)
    # Get the objects most recent information on azimuth and altitude.
    starCoordinates=cm.getHipApparantCoordinate(selectedItem.id,gpsManager.rtcDateTime)
    print(starCoordinates)
    actionText=selectedItem.name  + "\n" + selectedItem.description + "\nAzimuth: " + str(starCoordinates.get("azimuth").degrees)[:4] + "\nAltitude: " + str(starCoordinates.get("altitude").degrees)[:4] 
    display.showText(actionText)
    gm.move(starCoordinates.get("azimuth").degrees,starCoordinates.get("altitude").degrees)
    time.sleep(5)

def doPlanets():
    menuItems = []
    for index,planet in enumerate(cm.planets):
        # Only show constellations that are abouve the horizon
        if planet.altitude>settingsManager.get_setting("PLANET_ALTITUDE_CUTOFF"):
            menuItems.append(MenuItem(planet.name ,index, "",  planet.azimuth, planet.altitude, 0,0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    print(selectedItem)
    # Get the objects most recent information on azimuth and altitude.
    print(selectedItem.id,cm.planets[selectedItem.id].planet)
    planetCoordinates=cm.getPlanetApparantCoordinate(cm.planets[selectedItem.id].planet,gpsManager.rtcDateTime)
    print(planetCoordinates)
    actionText=selectedItem.name  + "\n" + "\nAzimuth: " + str(planetCoordinates.get("azimuth").degrees)[:4] + "\nAltitude: " + str(planetCoordinates.get("altitude").degrees)[:4] 
    display.showText(actionText)
    gm.move(planetCoordinates.get("azimuth").degrees,planetCoordinates.get("altitude").degrees)
    time.sleep(5)

# Main code
while True:
    print("RTC datetime:",gpsManager.rtcDateTime)
    selectedItem=doStartMenu()
    if selectedItem.name =="Setup":
        doSetup()
    if selectedItem.name =="Stars":
        doStars()
    if selectedItem.name =="Constellations":
        doConstellations()
    if selectedItem.name =="Planets":
        doPlanets()
    if selectedItem.name =="Exit":
        exit()

