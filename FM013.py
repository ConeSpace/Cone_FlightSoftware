#
#   TestMode 013
#   Read GPS Signal and print it
#
#


import time
import IMUGps
import Comm
import datetime


while True:
    
    time, lat, dirLat, lon, dirLon = IMUGps.fnc_IMU_Gps()
    
    msg = ("GPS Time: " + time + "UTC" + " Lat: " + lat + " " + dirLat + " Lon: " + lon + " " + dirLon)
    
    print(msg)
    
    ###SEND DATA###
    Comm.fnc_CommTransmit(msg)
    
    