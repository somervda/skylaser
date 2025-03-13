from skyfield.api import Star, load,  wgs84,utc,Angle, EarthSatellite
from skyfield.data import hipparcos
from skyfield.named_stars import named_star_dict
from settingsManager import SettingsManager
from datetime import datetime,timedelta,timezone
import time
import csv

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

class Satellite():
    def __init__(self,name,satellite,description,azimuth,altitude):
        self._name = name
        self._satellite=satellite
        self._description=description
        self._azimuth=azimuth
        self._altitude=altitude  

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def satellite(self):
        return self._satellite
    
    @satellite.setter
    def satellite(self, satellite):
        self._satellite = satellite

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description
    
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


class Planet():
    def __init__(self,name,planet,azimuth,altitude):
        self._name = name
        self._planet=planet
        self._azimuth=azimuth
        self._altitude=altitude   

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def planet(self):
        return self._planet

    @planet.setter
    def planet(self, value):
        self._planet = value

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, value):
        self._azimuth = value

    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, value):
        self._altitude = value 

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
    def __init__(self,latitude,longitude,elevation,currentDateTime):
        self._settingsManager = SettingsManager("settings.json")
        self._latitude = latitude
        self._longitude = longitude
        self._elevation = elevation
        self._currentDateTime = currentDateTime

        # Load the ephameris for planets first. Information about the earth is
        # required for calculations
        print("Loading ephameris from  from de421.bsp")
        self._eph = load('de421.bsp')
        # Use hipparcos data hip_main.dat
        # Load to pandas dataframe - see https://pandas.pydata.org/docs/getting_started/overview.html 
        print("Loading dataframe from hip_main.dat")
        with open('/home/pi/skylaser/hip_main.dat', 'r') as f:     
            self._df = hipparcos.load_dataframe(f)

        # Build lists of celestrial objects
        self.buildSatellites()
        # Save a list of brightStars
        self._brightStars=self.getBrightStars()
        # Create a list of the main constilations
        self.buildConstellations()
        # Build a list of planets
        self.buildPlanets()



    @property
    def planets(self): 
        return self._planets

    @property
    def satellites(self): 
        return self._satellites

    @property
    def constellations(self): 
        return self._constellations

    @property
    def brightStars(self): 
        return self._brightStars

    def buildSatellites(self):
        # Build a list of important satellites 
        print("loading ephameris from satellites.csv")
        with load.open('satellites.csv', mode='r') as f:
            satData = list(csv.DictReader(f))
        print("Building Satellites...")
        self._satellites=[]
        self.makeSatellite("HST",satData,"Hubble Space Telescope")
        self.makeSatellite("ISS (ZARYA)",satData,"International Space Station")
        self.makeSatellite("CSS (TIANHE)",satData,"Chinese Space Station")
        self.makeSatellite("VIASAT-1",satData,"Large Canadian Com. Sat. \nGeosyncronous")
        self.makeSatellite("STARLINK-1073",satData,"Starlink")
        self.makeSatellite("STARLINK-1202",satData,"Starlink")
        self.makeSatellite("STARLINK-5498",satData,"Starlink ")
        self.makeSatellite("STARLINK-30284",satData,"Starlink ")
        self.makeSatellite("STARLINK-32907",satData,"Starlink ")
        self.makeSatellite("STARLINK-31495",satData,"Starlink ")
        self.makeSatellite("STARLINK-11407 [DTC]",satData,"Starlink ")
        self.makeSatellite("LANDSAT 9",satData,"U.S. Geological Survey 2021")
        self.makeSatellite("NAVSTAR 68 (USA 242)",satData,"GPS")
        self.makeSatellite("GPS BIIF-6 (PRN 06)",satData,"GPS")
        self.makeSatellite("GPS BIIRM-1 (PRN 17)",satData,"GPS")
        self.makeSatellite("IRIDIUM 139",satData,"Sat. phone (LEO)")
        self.makeSatellite("SES-5",satData,"Sirius Radio - Sirius 5")
        self.makeSatellite("AMC-3",satData,"Commercial broadcasts\nGeosyncronous")


    def makeSatellite(self,name,satData,description):
        # Add details about apparent position of the satellite, if the satellite is 
        # abouve the horizon then add it to the satellite list
        ts = load.timescale()
        satellites = [EarthSatellite.from_omm(ts, fields) for fields in satData]
        for sat in satellites:
            if sat.name == name:
                apparent = self.getSatelliteApparantCoordinate(sat)
                # Above the cuttoff angle?
                if apparent.get("altitude").degrees>self._settingsManager.get_setting("SATELLITE_ALTITUDE_CUTOFF"):
                    self._satellites.append(Satellite(name,sat,description,apparent.get("azimuth").degrees,apparent.get("altitude").degrees))
                    return True
                else:
                    # print(name," is too low, not added.",apparent.get("azimuth").degrees,apparent.get("altitude").degrees)
                    return False
        # print("Not found:",name)
        return False

    def getSatelliteApparantCoordinate(self,satellite,currentDateTime=None):
        # Create a timescale and ask the current time.
        # Optionally can use different datetime from when the object was created
        if currentDateTime==None:
            currentDateTime = self._currentDateTime
        ts = load.timescale()
        t = ts.from_datetime(currentDateTime.replace(tzinfo=utc))
        myLocation =  self._eph['earth'] +  wgs84.latlon(self._latitude , self._longitude , elevation_m=self._elevation)
        satPosition =  self._eph['earth'] +  satellite
        alt, az, d = myLocation.at(t).observe(satPosition).apparent().altaz()
        return {"altitude":alt,"azimuth":az,"distance":d}

    def buildConstellations(self):
        print("Building Constellations...")
        self._constellations=[]
        self._constellations.append(Constellation('Orion  ','Rigel  ','The Hunter',24436,0,0))
        self._constellations.append(Constellation('Ursa Major','Dubhe  ','Big Dipper ',54061,0,0))
        self._constellations.append(Constellation('Ursa Minor','Polaris  ','Little Dipper ',11767,0,0))
        self._constellations.append(Constellation('Cassiopeia ','Schedar','The queen of Aethiopia',3179,0,0))
        self._constellations.append(Constellation('Cygnus','Deneb ','The Swan',102098,0,0))
        self._constellations.append(Constellation('Canis Major','Sirius','The Big Dog',32349,0,0))
        self._constellations.append(Constellation('Canis Minor  ','Procyon','The Little Dog',37279,0,0))
        self._constellations.append(Constellation('Pegasus','Algenib','The Winged Horse ',1067,0,0))
        self._constellations.append(Constellation('Taurus','Aldebaran','The Bull Loyal, honest\nand hard-working\nApril 20 - May 20',21421,0,0))
        self._constellations.append(Constellation('Gemini','Pollux','The Twins Adaptable\nperceptive and curious\nMay 21 - June 21',37826,0,0))
        self._constellations.append(Constellation('Leo','Regulus',' The Lion Confident\nleaders and action-orented\nJuly 23 - Aug 22',49669,0,0))
        self._constellations.append(Constellation('Virgo','Spica','The Maiden Perfectionists\nlogical and observant\nAug25 - Sept 22',65474,0,0))
        self._constellations.append(Constellation('Scorpius','Antares','The Scorpion Intense\npassionate and mysterious\nOct 23 - Nov 21',80763,0,0))
        self._constellations.append(Constellation('Sagittarius','Kaus Austrina',' The Archer\nOptimistic, adventurous\nNov 22 - Dec 21',90185,0,0))
        self._constellations.append(Constellation('Capricornus ','Diphda','The Goat Hardworking\npractical, and ambitious\nDec 22 - Jan 19 ',3419,0,0))
        self._constellations.append(Constellation('Aquarius ','Sadr','The Water Bearer Independent\ncreative, and humanitarian\nJan 20 - Feb 18',100453,0,0))
        self._constellations.append(Constellation('Pisces','Alpherg','The Fish Creative\nimaginative,kind and empathetic\nFebruary 19 to March 20',7097,0,0))
        self._constellations.append(Constellation('Libra','Beta Librae','The Scales Sociable\ncharming, and diplomatic\nSept 23 and Oct 22',74785,0,0))
        self._constellations.append(Constellation('Aries','Hamal','The Ram Bold\nambitious, and competitive\nMarch 21 - April 19',9884,0,0))
        self._constellations.append(Constellation('Cancer','Tarf','The Crab Intuitive\nnurturing, and emotional\nJune 22 - July 22',40526,0,0))
        for constellation in self._constellations:
            apparant =self.getHipApparantCoordinate(constellation.hipId,currentDateTime=None)
            constellation.azimuth=apparant.get("azimuth").degrees
            constellation.altitude=apparant.get("altitude").degrees

    def buildPlanets(self):
        print("Building planets...")
        self._planets=[]
        self._planets.append(Planet("Mercury",self._eph['Mercury Barycenter'],0,0))
        self._planets.append(Planet("Venus",self._eph['Venus Barycenter'],0,0))
        self._planets.append(Planet("Mars",self._eph['Mars Barycenter'],0,0))
        self._planets.append(Planet("Jupiter",self._eph['Jupiter Barycenter'],0,0))
        self._planets.append(Planet("Saturn",self._eph['Saturn Barycenter'],0,0))
        self._planets.append(Planet("Uranus",self._eph['Uranus Barycenter'],0,0))
        self._planets.append(Planet("Neptune",self._eph['Neptune Barycenter'],0,0))
        self._planets.append(Planet("Sun",self._eph['Sun'],0,0))
        self._planets.append(Planet("Moon",self._eph['Moon'],0,0))
        for planet in self._planets:
            apparent = self.getPlanetApparantCoordinate(planet.planet)
            planet.altitude=apparent.get("altitude").degrees
            planet.azimuth=apparent.get("azimuth").degrees

    def getPlanetApparantCoordinate(self,planet,currentDateTime=None):
        # Create a timescale and ask the current time.
        # Optionally can use different datetime from when the object was created
        if currentDateTime==None:
            currentDateTime = self._currentDateTime
        ts = load.timescale()
        t = ts.from_datetime(currentDateTime.replace(tzinfo=utc))
        myLocation = self._eph['earth'] + wgs84.latlon(self._latitude , self._longitude , elevation_m=self._elevation)
        myAstrometric = myLocation.at(t).observe(planet)
        alt, az, d = myAstrometric.apparent().altaz()
        return {"altitude":alt,"azimuth":az,"distance":d}

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
        myLocation = self._eph['earth'] + wgs84.latlon(self._latitude , self._longitude , elevation_m=self._elevation)
        myAstrometric = myLocation.at(t).observe(myStar)
        # alt, az, d = myAstrometric.apparent().altaz()
        alt, az, d = myAstrometric.apparent().altaz()
        return {"altitude":alt,"azimuth":az,"distance":d}

    def getBrightStars(self):
        # Filter stars based on magnitude 
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
    # for itemName, itemHip in named_star_dict.items():
    #     print(itemName,itemHip)
    # exit()
    # Load class and create celestral object lists
    cm=CelestialManager(40.1748,-75.302,5000,datetime.utcnow())
    print("Stars")
    for star in cm.brightStars:
        print(star.name,star.id,star.magnitude,star.azimuth,star.altitude,star.distance)
    print("\nConstellations")
    for constellation in cm.constellations:
        print(constellation.name,constellation.description,constellation.azimuth,constellation.altitude)
    print("\nPlanets")
    for planet in cm.planets:
        print(planet.name,planet.azimuth,planet.altitude)
    print("\nSatellites")
    for satellite in cm.satellites:
        print(satellite.name,satellite.description,satellite.azimuth,satellite.altitude)