from skyfield.api import Star, load,  wgs84,utc,Angle
from skyfield.data import hipparcos
from skyfield.named_stars import named_star_dict
from settingsManager import SettingsManager
from datetime import datetime,timedelta,timezone
import time

class CelestrialInfo(): 
    def __init__(self,name,id,magnitude,azimuth,altitude,distance):
        self._name = name
        self._id = id
        self._magnitude = magnitude
        self._azimuth =azimuth
        self._altitude = altitude
        self._distance=distance
    
    @property
    def name(self): 
        return self._name

    @property
    def id(self): 
        return self._id
    
    @property
    def magnitude(self): 
        return self._magnitude
    
    @property
    def azimuth(self): 
        return self._azimuth
    
    @property
    def altitude(self): 
        return self._altitude
    
    @property
    def distance(self): 
        return self._distance
    

class CelestialManager():
    def __init__(self,settingFile,latitude,longitude,elevation,currentDateTime,reload=False):
        self._settingsManager = SettingsManager(settingFile)
        self._latitude = latitude
        self._longitude = longitude
        self._elevation = elevation
        self._currentDateTime = currentDateTime

        self._planets = load('de421.bsp')
        if reload :
            # Get a new copy of the hipparcos data 
            # needs internet access to work
            # Load to pandas dataframe 
            with load.open(hipparcos.URL) as f:
                print("loading dataframe from internet...")
                self._df = hipparcos.load_dataframe(f)
        else:
            # Use hipparcos data hip_main.dat
            # Load to pandas dataframe - see https://pandas.pydata.org/docs/getting_started/overview.html 
            with open('/home/pi/skylaser/hip_main.dat', 'r') as f:     # Do something with the file here
                print("loading dataframe from hip_main.dat")
                self._df = hipparcos.load_dataframe(f)
        # Save a list of brightStars
        self._brightStars=self.getBrightStars()


    @property
    def brightStars(self): 
        return self._brightStars

    def getHipName(self,hip):
        for itemName, itemHip in named_star_dict.items():
            if hip == itemHip:
                return itemName
        return "*" + str(hip)

    def getHipApparantCoordinate(self,hipId,currentDateTime=None):
        # Create a timescale and ask the current time.
        # Optionally can use different datetime from when the object was created
        if currentDateTime==None:
            currentDateTime = self._currentDateTime
        ts = load.timescale()
        t = ts.from_datetime(currentDateTime.replace(tzinfo=utc))
        myStar= Star.from_dataframe(self._df.loc[hipId])
        # print("lat:",self.latitude,"lng:",self.longitude)
        myLocation = self._planets['earth'] + wgs84.latlon(self._latitude , self._longitude , elevation_m=self._elevation)
                 
        myAstrometric = myLocation.at(t).observe(myStar)
        # alt, az, d = myAstrometric.apparent().altaz()
        alt, az, d = myAstrometric.apparent().altaz()
        return {"altitude":alt,"azimuth":az,"distance":d}


    def getBrightStars(self):
        # Filter based on magnitude 
        print("getBrightStars")
        magnitude_cutoff=self._settingsManager.get_setting("STAR_MAGNITUDE_CUTOFF")
        brightStars = self._df.query('magnitude <= @magnitude_cutoff')
        stars=[]
        for index, row in brightStars.iterrows():
            apparantInfo=self.getHipApparantCoordinate(index)
            # Only show stars that are a specified number of degrees abouve the horizon
            if apparantInfo.get("altitude").degrees>self._settingsManager.get_setting("STAR_ALTITUDE_CUTOFF"):
                stars.append(CelestrialInfo(self.getHipName(index),index,row['magnitude'],apparantInfo.get("azimuth"),apparantInfo.get("altitude"),apparantInfo.get("distance")))
        return sorted(stars, key=lambda x: x.name)

        


if __name__ == "__main__":
    # Load class and create celestral object lists
    cm=CelestialManager("/home/pi/skylaser/settings.json",40.1748,-75.302,5000,datetime.now(),reload=False)
    for star in cm.brightStars:
        print(star.name,star.id,star.magnitude,star.azimuth,star.altitude,star.distance)