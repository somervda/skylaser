import serial
import time
import string 
import pynmea2
from datetime import datetime, timezone
#  see https://github.com/Knio/pynmea2

port="/dev/serial0"
ser=serial.Serial(port,baudrate=9600,timeout=0.5)

class GPSManager:
    def __init__(self):
        self.readGPS()

    def readGPS(self):
        self._latitude = None
        self._longitude = None
        self._altitude = None
        self._timestamp = None
        self._datetime = None
        self._isValid = False
        # Will read the gps stream until all required values have been recieved
        print("readGPS...")
        startTime= time.time()
        while not (self._longitude and self._latitude and self._altitude and self._datetime ): 
            if time.time()-startTime>180:
                print("GPS timeout")
                return False
            newdata=ser.readline().decode('utf-8')
            if newdata[0:3]=="$GP":
                dataout =pynmea2.NMEAStreamReader()
                msg=pynmea2.parse(newdata)
                if hasattr(msg, 'datetime'):
                    print( msg.datetime)
                    self._datetime = datetime.fromisoformat(str(msg.datetime))
                    # dateTimeSTR = str(msg.datetime.date()) + " " +str(msg.datetime.time())
                    # print("dateTimeSTR:",dateTimeSTR)
                    # datetime_object = datetime.strptime(dateTimeSTR, "%Y-%m-%d %H:%M:$S")
                    print(self._datetime)
                if hasattr(msg, 'altitude'):
                    self._altitude = msg.altitude
                if hasattr(msg, 'latitude'):
                    self._latitude = msg.latitude
                if hasattr(msg, 'longitude'):
                    self._longitude = msg.longitude
        self._isValid = True
        # Find the delta between the real time clock and the GPS to be able
        # to get the rtc based datetime based on a correction between the GPS and basic RTC time
        # This is needed because the rtc usually is only set when the PIZero is connect to the internet
        self._rtcDeltaSeconds = self._datetime - datetime.now((timezone.utc)) 
        print("GPS:",self._datetime," RTC:",datetime.now((timezone.utc))," Delta:",self._rtcDeltaSeconds )
        return True

    @property
    def latitude(self): 
        return self._latitude

    @property
    def longitude(self): 
        return self._longitude

    @property
    def altitude(self): 
        return self._altitude

    @property
    def datetime(self): 
        # Date as a dattime object
        return self._datetime
        
    @property
    def timestamp(self): 
        # Seconds since the start of the unix epoch 
        return self._datetime.timestamp()

    @property
    def rtcDateTime(self):
        # Return a datatime that is sourced from the real time clock but been adjusted
        # to compensate for differences between the rtc and gps times
        rtc=datetime.now((timezone.utc))
        # print("RTC datetime adjusted based on GPS:",rtc + self._rtcDeltaSeconds, " (rtc:",rtc,")")
        return rtc + self._rtcDeltaSeconds

    @property
    def isValid(self):
        # Has succesfully collected GPS data
        return self._isValid
