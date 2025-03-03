from gpsManager import GPSManager
gpsManager=GPSManager()

print("getting GPS data")
if gpsManager.readGPS() :
    print(gpsManager.latitude , gpsManager.longitude , gpsManager.altitude , gpsManager.datetime , gpsManager.timestamp)
else:
    print("gps read failed")
