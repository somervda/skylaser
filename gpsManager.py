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
        pass

    def readGPS(self):
        self._latitude = None
        self._longitude = None
        self._elevation = None
        self._timestamp = None
        self._datetime = None
        # Will read the gps stream until all required values have been recieved
        print("readGPS...")
        startTime= time.time()
        while not (self._longitude and self._latitude and self._elevation and self._datetime ): 
            duration = time.time()-startTime
            if not(self._elevation) and  duration>30:
                # Elevation is hard to calculate by gps, if no found after 30 seconds  then 
                # just set it to 0.1
                print("gpsManager: gave up and set elevation to 0.1")
                print("duration:",duration,self._elevation)
                self._elevation=0.1
            if duration>60:
                print("GPS timeout")
                print("duration:",duration)
                return False
            # Sometime get a -
            # 'utf-8' codec can't decode byte 0x89 in position 1: invalid start byte
            # just skip error and read next time we come around
            try:
                newdata=ser.readline().decode('utf-8')
            except Exception as e:
                print("gpsManager, error reading newdata:",e)
                newdata="     "
            if newdata[0:3]=="$GP":
                # print("* ",datetime.now(),self._longitude,self._latitude,self._elevation,self._datetime)
                # print(newdata)
                dataout =pynmea2.NMEAStreamReader()
                msg=pynmea2.parse(newdata)
                try:
                    if hasattr(msg, 'datetime'):
                        self._datetime = datetime.fromisoformat(str(msg.datetime))
                except Exception as e:
                    # Report and Ignore if we have an error
                    print("hasattr(msg, 'datetime') error",e)
                if hasattr(msg, 'altitude'):
                    if msg.altitude:
                        self._elevation = msg.altitude
                if hasattr(msg, 'latitude'):
                    if msg.latitude!=0:
                        self._latitude = msg.latitude
                if hasattr(msg, 'longitude'):
                    if msg.longitude!=0:
                        self._longitude = msg.longitude
        # Find the delta between the real time clock and the GPS to be able
        # to get the rtc based datetime based on a correction between the GPS and basic RTC time
        # This is needed because the rtc usually is only set when the PIZero is connect to the internet
        self._rtcDeltaSeconds = self._datetime - datetime.now((timezone.utc)) 
        print("GPS:",self._longitude,self._latitude," Elevation:",self._elevation," datetime:",self._datetime )
        return True

    @property
    def latitude(self): 
        return self._latitude

    @property
    def longitude(self): 
        return self._longitude

    @property
    def elevation(self): 
        return self._elevation

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



if __name__ == "__main__":
    gpsManager=GPSManager()
    print("getting GPS data")
    if gpsManager.readGPS() :
        print("Lat:",gpsManager.latitude ," Lng:", gpsManager.longitude , " Elevation:",gpsManager.elevation , " datetime:",gpsManager.datetime ," Epoch seconds:", gpsManager.timestamp)
    else:
        print("gps read failed")
