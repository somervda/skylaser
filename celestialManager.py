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

class Constellation():
    def __init__(self,name,starName,description,hipId,azimuth,altitude):
        self._name = name
        self._starName = starName
        self._description=description
        self._hipId=hipId
        self._azimuth=azimuth
        self._altitude=altitude
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def starName(self):
        return self._starName

    @starName.setter
    def starName(self, starName):
        self._starName = starName

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def hipId(self):
        return self._hipId

    @hipId.setter
    def hipId(self, hipId):
        self._hipId = hipId

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, azimuth):
        self._azimuth = azimuth

    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, altitude):
        self._altitude = altitude

class CelestialManager():
    def __init__(self,latitude,longitude,elevation,currentDateTime,reload=False):
        self._settingsManager = SettingsManager("settings.json")
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
        # Create a list of the main constilations
        self._constellations=[]
        self._constellations.append(Constellation('Orion  ','Rigel  ','The Hunter',24436,0,0))
        self._constellations.append(Constellation('Ursa Major','Dubhe  ','Big Dipper ',54061,0,0))
        self._constellations.append(Constellation('Ursa Minor','Polaris  ','Little Dipper ',11767,0,0))
        self._constellations.append(Constellation('Cassiopeia ','Schedar','The queen of Aethiopia',3179,0,0))
        self._constellations.append(Constellation('Cygnus ','Deneb ','The Swan ',102098,0,0))
        self._constellations.append(Constellation('Canis Major ) ','Sirius  ','The Big Dog',32349,0,0))
        self._constellations.append(Constellation('Canis Minor  ','Procyon  ','The Little Dog',37279,0,0))
        self._constellations.append(Constellation('Taurus  ','Aldebaran  ','The Bull',21421,0,0))
        self._constellations.append(Constellation('Gemini  ','Pollux  ','The Twins',37826,0,0))
        self._constellations.append(Constellation('Leo ','Regulus  ',' The Lion',49669,0,0))
        self._constellations.append(Constellation('Virgo ','Spica  ','The Maiden ',65474,0,0))
        self._constellations.append(Constellation('Scorpius ','Antares  ','The Scorpion ',80763,0,0))
        self._constellations.append(Constellation('Sagittarius','Kaus Austrina  ',' The Archer ',90185,0,0))
        self._constellations.append(Constellation('Capricornus ','Diphda  ','The Goat ',3419,0,0))
        self._constellations.append(Constellation('Aquarius ','Sadr  ','The Water Bearer ',100453,0,0))
        self._constellations.append(Constellation('Pisces ','Alpherg','The Fish ',7097,0,0))
        self._constellations.append(Constellation('Pegasus ','Algenib  ','The Winged Horse ',1067,0,0))
        for constellation in self._constellations:
            apparant =self.getHipApparantCoordinate(constellation.hipId,currentDateTime=None)
            # print(constellation.name,apparant)
            constellation.azimuth=apparant.get("azimuth").degrees
            constellation.altitude=apparant.get("altitude").degrees
            # print(constellation.name,constellation.azimuth,constellation.altitude)


    @property
    def constellations(self): 
        return self._constellations

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
    cm=CelestialManager(40.1748,-75.302,5000,datetime.now(),reload=False)
    for star in cm.brightStars:
        print(star.name,star.id,star.magnitude,star.azimuth,star.altitude,star.distance)

    for constellation in cm.constellations:
        print(constellation.name,constellation.description,constellation.azimuth,constellation.altitude)