import time
import os
from menu import Display,MenuItem
from datetime import datetime
from gpsManager import GPSManager
from gimbalManager import GimbalManager
from celestialManager import CelestialManager
from settingsManager import SettingsManager
from downloadManager import DownloadManager

print("\n\nStarting Skylaser")

# Initializations
dm=DownloadManager()
hasInternet=dm.checkInternet()
display= Display()

# Check required data files exist
if not (os.path.exists("de421.bsp") and os.path.exists("hip_main.dat") and os.path.exists("satellites.csv")):
    if hasInternet:
        display.showText("Downloading missing\nfiles...")
        dm.downloadHippacos()
        dm.downloadDe421()
        dm.downloadSatellites()
    else:
        display.showText("A file is missing.\nYou are not connected\nto the internet\nConnect to internet\nto load files.")
        time.sleep(10)
        exit()



display.showText("Starting SkyLaser...\nhasInternet:" + str(hasInternet))
gm=GimbalManager()
settingsManager=SettingsManager("settings.json")

# Need GPS info to initialize the starFinder
display.showText("Getting GPS...")
gpsLooper=0
gpsManager=GPSManager()
for retry in range(4):
    print("gpsLooper:",str(gpsLooper))
    try:
        if gpsManager.readGPS():
            print(gpsManager.latitude , gpsManager.longitude , gpsManager.elevation , gpsManager.datetime , gpsManager.timestamp)
            gpsInfoText = "Latitude: " + str(gpsManager.latitude)[:7] +"\nLongitude: " + str(gpsManager.longitude)[:7] + "\nDate (GMT): " + str(gpsManager.datetime)[:10] + "\nTime (GMT): " + str(gpsManager.datetime)[11:19] 
            print(gpsInfoText)
            display.showText(gpsInfoText)
            time.sleep(2)
            break
        else:
            gpsLooper+=1
            exceptMsg="Timed out\nTrying again: "  + str(gpsLooper)
            display.showText(exceptMsg )
            print(exceptMsg )
            time.sleep(5)           
    except Exception as e:
        gpsLooper+=1
        exceptMsg="Exception connection\nto GPS\nTrying again: "  + str(gpsLooper)
        display.showText(exceptMsg )
        print(exceptMsg ,e)
        time.sleep(5)
print("gpsLooper x:",str(gpsLooper))
if gpsLooper==4 :
        display.showText("Error\nFailed connection to GPS\nExiting")
        time.sleep(5)
        exit()
        


display.showText("Loading celestial data...")  
cm=CelestialManager(gpsManager.latitude,gpsManager.longitude ,gpsManager.elevation,gpsManager.rtcDateTime)

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
    menuItems.append(MenuItem("Move to 90,0",1, "", 90, 0, 0, 0))
    menuItems.append(MenuItem("Move to 180,0",2, "", 180, 0, 0, 0))
    menuItems.append(MenuItem("Move to 270,0", 3,"", 270, 0, 0, 0))
    menuItems.append(MenuItem("Move to 0,45",4, "", 0, 45, 0, 0))
    menuItems.append(MenuItem("Move to 90,45",5, "", 90, 45, 0, 0))
    menuItems.append(MenuItem("Move to 180,45",6, "", 180, 45, 0, 0))
    menuItems.append(MenuItem("Move to 270,45",7, "", 270, 45, 0, 0))
    menuItems.append(MenuItem("Move to 0,90", 8,"", 0, 90, 0, 0))
    menuItems.append(MenuItem("Walk Sky", 9,"", 0, 0, 0, 0))
    if hasInternet:
        menuItems.append(MenuItem("Download Data...", 10,"", 0, 0, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    if selectedItem.id<=8:
        gm.move(selectedItem.azimuth,selectedItem.altitude)
    if selectedItem.id==9:
        display.showText("Walking the sky...")
        for azimuth in range(0,360,45):
            for altitude in range(0,100,45):
                gm.move(azimuth,altitude)
        gm.move(0,0)
    if selectedItem.id==10:
        display.showText("Getting Hippacos...")
        dm.downloadHippacos()
        display.showText("Getting De421...")
        dm.downloadDe421()

def doStars():
    menuItems = []
    for brightStar in cm.brightStars:
        menuItems.append(MenuItem(brightStar.name + " " + str(brightStar.magnitude) ,brightStar.id, "", brightStar.azimuth, brightStar.altitude, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    print(selectedItem)
    # Get the objects most recent information on azimuth and altitude.
    starCoordinates=cm.getHipApparantCoordinate(selectedItem.id,gpsManager.rtcDateTime)
    print(starCoordinates)
    actionText=selectedItem.name  + "\nAzimuth: " + str(starCoordinates.get("azimuth").degrees)[:5] + "\nAltitude: " + str(starCoordinates.get("altitude").degrees)[:4] 
    display.showText(actionText)
    gm.move(starCoordinates.get("azimuth").degrees,starCoordinates.get("altitude").degrees)
    time.sleep(5)

def doConstellations():
    menuItems = []
    for index,constellation in enumerate(cm.constellations):
        # Only show constellations that are abouve the horizon
        if constellation.altitude>settingsManager.get_setting("CONSTELLATION_ALTITUDE_CUTOFF"):
            menuItems.append(MenuItem(constellation.name ,index, constellation.description, constellation.azimuth, constellation.altitude, 0, 0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    print(selectedItem)
    # Get the objects most recent information on azimuth and altitude.
    starCoordinates=cm.getHipApparantCoordinate(cm.constellations[selectedItem.id].hipId,gpsManager.rtcDateTime)
    print(starCoordinates)
    actionText=selectedItem.name  + " - " + cm.constellations[selectedItem.id].starName + "\n" + selectedItem.description + "\nAz: " + str(starCoordinates.get("azimuth").degrees)[:5] + " Alt: " + str(starCoordinates.get("altitude").degrees)[:4] 
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
    actionText=selectedItem.name  + "\n" + "\nAzimuth: " + str(planetCoordinates.get("azimuth").degrees)[:5] + "\nAltitude: " + str(planetCoordinates.get("altitude").degrees)[:4] 
    display.showText(actionText)
    gm.move(planetCoordinates.get("azimuth").degrees,planetCoordinates.get("altitude").degrees)
    time.sleep(5)

def doSatellites():
    menuItems = []
    for index,satellite in enumerate(cm.satellites):
        menuItems.append(MenuItem(satellite.name ,index, "",  0, 0, 0,0))
    display.menuItems = menuItems
    selectedItem = display.showMenu()
    # Get the objects most recent information on azimuth and altitude.
    print(selectedItem.id,cm.satellites[selectedItem.id].name)
    # Get the current coordinates for the selectedsatellite (They change quickly)
    satelliteCoordinates=cm.getSatelliteApparantCoordinate(cm.satellites[selectedItem.id].satellite,gpsManager.rtcDateTime)
    print(satelliteCoordinates)
    if satelliteCoordinates.get("altitude").degrees>0:
        actionText=selectedItem.name  + "\n" + cm.satellites[selectedItem.id].description + "\nAzimuth: " + str(satelliteCoordinates.get("azimuth").degrees)[:5] + "\nAltitude: " + str(satelliteCoordinates.get("altitude").degrees)[:4] 
        display.showText(actionText)
        gm.move(satelliteCoordinates.get("azimuth").degrees,satelliteCoordinates.get("altitude").degrees)
    else: 
        actionText=selectedItem.name  + "\nIs gone below the\nhorizon" 
        display.showText(actionText)
    time.sleep(5)



# Main code
while True:
    print("RTC datetime:",gpsManager.rtcDateTime)
    selectedItem=doStartMenu()
    if selectedItem.name =="Setup":
        doSetup()
    if selectedItem.name =="Stars":
        doStars()
    if selectedItem.name =="Satellites":
        doSatellites()
    if selectedItem.name =="Constellations":
        doConstellations()
    if selectedItem.name =="Planets":
        doPlanets()
    if selectedItem.name =="Exit":
        exit()

