from skyfield.api import Star, load,  wgs84,utc
from skyfield.data import hipparcos
from skyfield.named_stars import named_star_dict
from settingsManager import SettingsManager
from datetime import datetime,timedelta,timezone
import time

class StarInfo(): 
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
    

class StarFinder():
    def __init__(self,settingFile,latitude,longitude,currentDateTime,reload=False):
        self.settingsManager = SettingsManager(settingFile)
        self.latitude = latitude
        self.longitude = longitude
        self.currentDateTime = currentDateTime

        self.planets = load('de421.bsp')
        if reload :
            # Get a new copy of the hipparcos data 
            # needs internet access to work
            # Load to pandas dataframe 
            with load.open(hipparcos.URL) as f:
                print("loading dataframe from internet...")
                self.df = hipparcos.load_dataframe(f)
        else:
            # Use hipparcos data hip_main.dat
            # Load to pandas dataframe - see https://pandas.pydata.org/docs/getting_started/overview.html 
            with open('/home/pi/skylaser/hip_main.dat', 'r') as f:     # Do something with the file here
                print("loading dataframe from hip_main.dat")
                self.df = hipparcos.load_dataframe(f)

    def getBarnard(self):
        barnards_star = Star.from_dataframe(self.df.loc[87937])

        print("loading de421.bsp")
        planets = load('de421.bsp')

        print("calculating barnards_star position")
        earth = planets['earth']

        ts = load.timescale()
        t = ts.now()
        astrometric = earth.at(t).observe(barnards_star)
        ra, dec, distance = astrometric.radec()
        print(ra)
        print(dec)

    def getStarName(self,hip):
        for itemName, itemHip in named_star_dict.items():
            if hip == itemHip:
                return itemName
        return "*" + str(hip)

    def getStarApparantCoordinate(self,hipId):
        # Create a timescale and ask the current time.
        ts = load.timescale()
        t = ts.from_datetime(self.currentDateTime.replace(tzinfo=utc))
        myStar= Star.from_dataframe(self.df.loc[hipId])
        print("lat:",self.latitude,"lng:",self.longitude)
        myLocation = self.planets['earth'] + wgs84.latlon(self.latitude , self.longitude )
                 
        myAstrometric = myLocation.at(t).observe(myStar)
        # alt, az, d = myAstrometric.apparent().altaz()
        alt, az, d = myAstrometric.apparent().altaz()
        return {"altitude":alt,"azimuth":az,"distance":d}


    def getBrightStars(self):
        # Filter based on magnitude 
        print("getBrightStars")
        magnitude_cutoff=self.settingsManager.get_setting("STAR_MAGNITUDE_CUTOFF")
        brightStars = self.df.query('magnitude <= @magnitude_cutoff')
        stars=[]
        for index, row in brightStars.iterrows():
            apparantInfo=self.getStarApparantCoordinate(index)
            # print("info:",index,apparantInfo)
            stars.append(StarInfo(self.getStarName(index),index,row['magnitude'],apparantInfo.get("azimuth"),apparantInfo.get("altitude"),apparantInfo.get("distance")))
            
            # print(index,self.getStarApparantCoordinate(index))
        return sorted(stars, key=lambda x: x.name)

        


if __name__ == "__main__":
    sf=StarFinder("/home/pi/skylaser/settings.json",40.1748,-75.302,datetime.now(),reload=False)
    for star in sf.getBrightStars():
        print(star.name,star.id,star.magnitude,star.azimuth,star.altitude,star.distance)