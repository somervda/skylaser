import serial
import time
import string 
import pynmea2
#  see https://github.com/Knio/pynmea2
lat = None
lng = None
altitude = None
time = None
date = None

port="/dev/serial0"
ser=serial.Serial(port,baudrate=9600,timeout=0.5)
while not (lat and lng and altitude and date and time): 
    newdata=ser.readline().decode('utf-8')
    if newdata[0:3]=="$GP":
        dataout =pynmea2.NMEAStreamReader()
        msg=pynmea2.parse(newdata)
        if hasattr(msg, 'datetime'):
            date = msg.datetime.date()
        if hasattr(msg, 'timestamp'):
            time = msg.timestamp
        if hasattr(msg, 'altitude'):
            altitude = msg.altitude
        if hasattr(msg, 'latitude'):
            lat = msg.latitude
        if hasattr(msg, 'longitude'):
            lng = msg.longitude

print(lat , lng , altitude , date , time)
